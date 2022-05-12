#!/usr/bin/env python3
#chmod +x /current/file

#let the cluster fuck begin

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
import os
import subprocess
import fileinput # for overwritesite()
import plistlib # for parsereadlist()
import pathlib # for calling itself in dlp()
import signal # to close dlp() terminal window
import yt_dlp # for dlp()
import requests # for aria()
import json # for aria()

def run(cmdstring): # string here because shell true because only way of chaning commands
    process = subprocess.run(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode())
    return process.stdout.decode()

def parsereadlist(): # when foldername not in downloaddir add url to aria or dlp dict
    run(f"plutil -convert xml1 -o {d['bookmarksxml']} {d['bookmarksplist']}") # TODO move this to setup/backup function
    plist = plistlib.load(open(d['bookmarksplist'], 'rb'))
    for child in plist['Children']:
        if child.get('Title', None) == 'com.apple.ReadingList':
            for item in child['Children']:
                foldername = (item['URIDictionary']['title'][:50] + item['URLString'][:20] + item['URLString'][20:]).replace('/','-').replace(':','-').replace('.','-').replace(' ','-')
                if foldername not in os.listdir(d['downpath']) and not item['URLString'].startswith('https://'): d['ariaurls'].append([foldername, item['URLString']]) # all not https into aria
                if foldername not in os.listdir(d['downpath']) and item['URLString'].startswith('https://') and not item['URIDictionary']['title'].startswith('vpn '): d['dlpurls'].append([foldername, item['URLString']]) # all https and not vpn to into dlp
                if item['URIDictionary']['title'].startswith('vpn '): d['vpnto'] = "connect " + item['URLString'][-2:] # vpn to country into d 'vpnto'

def vpnstatus(): # pipe vpn status into dict
    nicelist = run(d['sshpi'] + "nordvpn status").lstrip('\r-\r  \r\r-\r  \r').rstrip('\n').split('\n') # get vpn status and clean up output a bit
    for count, elem in enumerate(nicelist): d[nicelist[count].split(': ')[0]] = nicelist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value to dict

def overwritesite(): # rewrite site content corrosponding to vpnstatus()
    vpnstatus()
    d['ccode'] = d.get('Current server', "de")[:2] # get country then insert country code into css calss selector
    d['color'] = "#5cf287" if d['Status'] == 'Connected' else "#fc4444" # get on off color insert color part of css class selector
    d['line7'] = f"path.{d['ccode']} {{fill: {d['color']};}}  /* set color and ccode according to on off state */\n" # construct linnes
    d['line8'] = f"path.{d['ccode']}:hover {{stroke: {d['color']}; stroke-width: 4; fill: {d['color']};}}\n"
    for line in fileinput.input([os.path.join(d['puthere'], 'reposetories', 'spinala', 'index.html')], inplace=True): # open file and overwrite lines
        print(d['line7'], end='') if fileinput.filelineno() == 7 else print(d['line8'], end='') if fileinput.filelineno() == 8 else print(line, end='')

def pushsite(): # pull all repos and push changes of overwritesite()
    for r in d['repos']:
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git") # TODO move this to setup function
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', r)} pull") # gets changes from remote add --quiet to shut up TODO only pull spinala here rest perhaps in a complete back up funktion
        d['message']+= r + " "
    overwritesite() # update site content
    run(f"git -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} commit -am \"site update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} push ;" ) # commit -am does not picup on new created files

def setvpn():
    parsereadlist() # to get desired vpn location and urls
    run(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"))
    pushsite() # only depends on vpn status() not parrsereadlist()

def dlp():
    parsereadlist() # to get desired urls now in new process
    for url in d['dlpurls']:
        d['dlpopts']['outtmpl'] = os.path.join(d['downpath'], url[0], 'filename-vc:%(vcodec)s-ac:%(acodec)s.%(ext)s') # the first item in each url list is the foldername
        with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(url[1]) # the second item in each url list is the url
    os.kill(os.getppid(), signal.SIGHUP) # close window when done

    # TODO
    #   send message or sth on completion of each download
    #           #run(f"osascript -e 'tell application \"Messages\" to send \"site updated and pulled {d['message']}\" to participant \"{d['phonenr']}\"'") # send message site updated
    #   use internal merge/convert tool with ffmpeg to generate mp4




def aria(): # when called on download complete of aria d['ariaurls'] is empty so no urls added
    def send(data):
        try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
        except requests.exceptions.ConnectionError: run(f"aria2c {d['ariaopts']}") # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time
    for url in d['ariaurls']:
        send( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [url[1]], { 'dir': os.path.join(d['downpath'], url[0]) } ] } ) # send aria the url from lit url[1] and the dir with foldername from list url[0]

    send( {'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[{'methodName':'aria2.getGlobalStat'}, {'methodName': 'aria2.tellStopped', 'params':[0,20,['status', 'files', 'errorMessage']]}]]} )
    d['totalinaria'] = json.loads(d['r'].content)['result'][0][0].get('numActive') + json.loads(d['r'].content)['result'][0][0].get('numWaiting') 
    
    # all this only on dl completed
    for stopped in json.loads(d['r'].content)['result'][1][0]: # man im numb all this nested list dict shit braeks me here we want the first list in the second list in r content result list
        d['message'] = f"{stopped.get('status')} {stopped.get('errorMessage')[:80]}" # make message
        for fs in stopped.get('files', [{'path':'nofile'}]):
            d['message'] = f"{fs.get('path')} {d['message']}" 
            print(d['message']) # TODO send message here
            #    run(f"osascript -e 'tell application \"Messages\" to send \"site updated and pulled {d['message']}\" to participant \"{d['phonenr']}\"'") # send message site updated
  
    # evtl purge aria so next message is clean
        aria2.purgeDownloadResult

    #if no more to download meaning all done 
        aria2.shutdown

    # if succesful either aria made dir or I do cause aria is too slow
    # d['CurrentRelativeHumidity'] = how many downloads are in queue # tell homebridge aria count


def head():
    setvpn() # set vpn to location and psuhsite()
    
    # TODO FIRST THING OF ALL if vpn off shut aria down

    if d['Status'] == "Connected" and d['dlpurls'] and len(run("killall -s Python").split('kill')) == 2:  # +1 account for list.split always len 1 and +1 for Python currently running so this means if no dlp is up
        run(f"osascript -e 'tell app \"Terminal\" to do script \"{pathlib.Path(__file__).resolve()} dlp\" ' ") # call itself and bring dlp() up in new window
    
    if d['Status'] == "Connected" and d['ariaurls']:
        aria() # TODO

    print(d.get(sys.argv[3].strip("''") , 0)) # print aria count to homebridge
    sys.exit()

def test():
    setvpn()

#d = {'test': test, 'dlp': dlp, 'Get': head, # defs for running directly in cli via arguments
d ={'CurrentRelativeHumidity': 80, 'StatusActive': 1, 'StatusTampered': 0, # for homebridge
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned
    'puthere': '/Users/mini/Downloads/transfer/', # #put ./repos ./gists ./repos/ff/xmlbookmarks ./repos/ff/dwl-archive here
    'message': " ", # message to send
    'phonenr': privates.phone,
    'bookmarksxml': "/Users/mini/Desktop/SafariBookmarks.xml", # where to export bookmarks to
    'bookmarksplist': os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist'), # where apple stores bookmarks plist 
    'ariaurls': [['linuxiso' ,'magnet:?xt=urn:btih:9b4c1489bfccd8205d152345f7a8aad52d9a1f57&dn=archlinux-2022.05.01-x86_64.iso']],
    'dlpurls': [],
    'downpath': "/Users/mini/Desktop/", # path where to download to
    'dlpopts': {'simulate': False, 'restrict-filenames': False, 'ignoreerrors': True, 'format': 'bestvideo*,bestaudio', 'verbos': True, 'external_downloader': {'m3u8': 'aria2c'}},
    'ariaopts': f"--enable-rpc --rpc-listen-all --on-download-complete=/Users/mini/Desktop/ariahooktest.py --save-session=/Users/mini/Desktop/ariasfile.txt --input-file=/Users/mini/Desktop/ariasfile.txt --daemon=true --auto-file-renaming=false --allow-overwrite=false --seed-time=0",
}                                                           # TODO replace this ^ with {pathlib.Path(__file__).resolve()}
d.get(sys.argv[1].strip("''"), sys.exit)() # call head() with 'Get' from homebridge or TODO aria() on download completion of aria
