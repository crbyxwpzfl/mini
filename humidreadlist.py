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

def pluses(): # TODO debug
    for r in d['repos']: # out of pushsite() TODO only pull spinala here rest perhaps in a complete back up funktion
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git") # TODO move this to setup function
        print(f"cloned {r} to {os.path.join(d['puthere'], 'reposetories')}")
    
    run(f"plutil -convert xml1 -o {os.path.join(d['puthere'], 'reposetories', 'ff', 'SafariBookmarks.xml')} {os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')}") # out of parsereadlist() TODO move this to setup function

    # individualy working
    parsereadlist() # waht u want vpn location and urls
    print("parsed readlist")
    vpnstate() # where u are
    print("got vpn state")
    print("pulling changes overwriting site and pushhing site")
    pushsite()


def run(cmdstring): # string here because shell true because only way of chaning commands
    process = subprocess.run(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode()) # TODO make programm quiet
    return process.stdout.decode()

def parsereadlist(): # when foldername not in downloaddir add url to aria or dlp dict
    plist = plistlib.load(open(os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist'), 'rb'))
    for child in plist['Children']:
        if child.get('Title', None) == 'com.apple.ReadingList':
            for item in child['Children']:
                foldername = (item['URIDictionary']['title'][:50] + item['URLString'][:20] + item['URLString'][20:]).replace('/','-').replace(':','-').replace('.','-').replace(' ','-')
                if foldername not in os.listdir(d['puthere']) and not item['URLString'].startswith('https://'): d['ariaurls'].append([foldername, item['URLString']]) # all not https into aria
                if foldername not in os.listdir(d['puthere']) and item['URLString'].startswith('https://') and not item['URIDictionary']['title'].startswith('push vpn to '): d['dlpurls'].append([foldername, item['URLString']]) # all https and not vpn to into dlp
                if item['URIDictionary']['title'].startswith('push vpn to '): d['vpnto'] = "connect " + item['URLString'][-2:] # vpn to country into d 'vpnto'

def vpnstate(): # pipe vpn status into dict
    nicelist = run(d['sshpi'] + "nordvpn status").lstrip('\r-\r  \r\r-\r  \r').rstrip('\n').split('\n') # get vpn status and clean up output a bit
    for count, elem in enumerate(nicelist): d[nicelist[count].split(': ')[0]] = nicelist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value to dict

def overwritesite(): # overwrite site content corrosponding to parsereadlist() not vpnstate()
    d['color'] = "#fc4444" if d.get('vpnto', "Disconnected") == "Disconnected" else "#5cf287" # get on off color insert color part of css class selector
    d['line47'] = f'window.onload = load( \"{d.get("vpnto", "off")}\", \"{d["color"]}\", {int(12/len(d.get("vpnto", "lengthtwelfe")))} )\n' # pass site vpn loc and color and stroke width. css displays 'off' state just by color with css class selector, therefore germany has class 'de' and 'off' but js loads diferent icon for 'off' and 'de'
    for line in fileinput.input([os.path.join(d['puthere'], 'reposetories', 'spinala', 'index.html')], inplace=True): # open file and overwrite lines
        print(d['line47'], end='') if fileinput.filelineno() == 47 else print(line, end='')

def pushsite(): # pull all repos and push changes of overwritesite()
    run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} pull") # TODO gets changes from remote add --quiet to shut up 
    overwritesite() # update site content
    run(f"git -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} commit -am \"site update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} push ;" ) # commit -am does not picup on newly created files
    run(f"osascript -e 'tell application \"Messages\" to send \"pushed site to {d.get('vpnto', 'off')}\" to participant \"{d['phonenr']}\"'") # send message on site updated

def dlp(): # TODO perhaps use internal merge/convert tool with ffmpeg to generate mp4 and use archive at d['puthere']/repos/ff/dwl-archive
    parsereadlist() # to get desired urls now in new process here head() and paresreadlist never got called
    for url in d['dlpurls']:
        d['dlpopts']['outtmpl'] = os.path.join(d['puthere'], url[0], 'filename-vc:%(vcodec)s-ac:%(acodec)s.%(ext)s') # the first item in each url list is the foldername
        with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(url[1]) # the second item in each url list is the url
        run(f"osascript -e 'tell application \"Messages\" to send \"dlp done {url[0]}\" to participant \"{d['phonenr']}\"'") # send message site updated
    os.kill(os.getppid(), signal.SIGHUP) # close window when done

def sendaria(data):
        try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
        except requests.exceptions.ConnectionError: 
            if d['Status'] == "Connected": run(f"aria2c {d['ariaopts']}") # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time

def aria(): # TODO perhaps use more advanced opts add trackers and optimize concurrent downloads and save savefile every sec or so
    for url in d['ariaurls']: # on download completion call this bitsh empty so yeeet    smae for if not d['ariaurls'] at shutdown purge send message
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [url[1]], { 'dir': os.path.join(d['puthere'], url[0]) } ] } ) # send aria the url from lit url[1] and the dir with foldername from list url[0]
    sendaria( {'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[{'methodName':'aria2.getGlobalStat'}, {'methodName': 'aria2.tellStopped', 'params':[0,20,['status', 'files', 'errorMessage']]}]]} ) # retrive info of aria
    d['CurrentRelativeHumidity'] = json.loads(d['r'].content)['result'][0][0].get('numActive') + json.loads(d['r'].content)['result'][0][0].get('numWaiting') # all urls in aria
    for stopped in json.loads(d['r'].content)['result'][1][0]: # man im numb all this nested list dict shit braeks me here we want the first list in the second list in r content result list
        d['message'] = f"{stopped.get('status')} {stopped.get('errorMessage')[:80]}" # make message
        for fs in stopped.get('files', [{'path':'nofile'}]):
            d['message'] = f"{fs.get('path')} {d['message']}"
            if not d['ariaurls']: run(f"osascript -e 'tell application \"Messages\" to send \"aria {d['message']}\" to participant \"{d['phonenr']}\"'") # send message site updated
    if not d['ariaurls']: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.purgeDownloadResulti'} ) # purge aria so next message is clean shuld be save and shuld not make me miss anything
    if not d['ariaurls'] and d['CurrentRelativeHumidity'] == 0: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} ) #if no active and no waiting in queue shutdown aria 

def head():
    parsereadlist() # waht u want vpn location and urls
    vpnstate() # where u are
    if d.get('vpnto', "what u want")[:2] != d.get('Current server', "where u are")[:2]: run(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect")) # only set vpn when parsereadlist() vpn state not current vpnstate()
    if d.get('vpnto', "what u want")[:2] != d.get('Current server', "where u are")[:2]: pushsite() # only push site when parsereadlist() vpnstate not current vpnstate(). pushsite() itself sets site corrosponding to parsereadlist() not vpnstate()

    if len(run("killall -s aria2c").split('kill')) == 2 and d.get('Uptime', 'shiiit') == "shiiit": # prolly should not happen but yeah
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} )
        run(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'")

    if d.get('vpnto', "what u want")[:2] == d.get('Current server', "where u are")[:2] and d['Status'] == "Connected" and d['ariaurls']: # dont do aria() when parsereadlist() vpn state not vpnstate() eg off not stil on cause vpnstate() is lagging actual vpn is off and bunch others
        aria()

    if d.get('vpnto', "what u want")[:2] == d.get('Current server', "where u are")[:2] and d['Status'] == "Connected" and d['dlpurls'] and len(run("killall -s Python").split('kill')) == 2:  # +1 account for list.split always len 1 and +1 for Python currently running so this means if no dlp is up
        run(f"osascript -e 'tell app \"Terminal\" to do script \"{pathlib.Path(__file__).resolve()} dlp\" ' ") # call itself and bring dlp() up in new window

    print(d.get(sys.argv[3].strip("''") , int(len(d.get('Uptime', ''))/len(d.get('Uptime', '1'))) )) # print aria count to homebridge or print aria on as 'StatusActive' or calculate vpn on as 'StatusTampered' as in location tampered
    sys.exit()

d = {'debug': pluses,'Get': head, # defs for running directly in cli via arguments
    'CurrentRelativeHumidity': 80, 'StatusActive': len(run("killall -s aria2c").split('kill'))-1, # for homebridge
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned
    'puthere': '/Users/mini/Downloads/', # put d['puthere']/reposetories  d['puthere']/gists  d['puthere']/repos/ff/xmlbookmarks  here
    'message': " ", # message to send
    'phonenr': privates.phone,
    'ariaurls': [],
    'dlpurls': [],
    'dlpopts': {'simulate': False, 'restrict-filenames': False, 'ignoreerrors': True, 'format': 'bestvideo*,bestaudio', 'verbos': True, 'external_downloader': {'m3u8': 'aria2c'}},
    'ariaopts': f"--enable-rpc --rpc-listen-all --on-download-complete={pathlib.Path(__file__).resolve()} --save-session=/Users/mini/Desktop/ariasfile.txt --input-file=/Users/mini/Desktop/ariasfile.txt --daemon=true --auto-file-renaming=false --allow-overwrite=false --seed-time=0",
}
d.get(sys.argv[1].strip("''"), aria)() # call head() with 'Get' from homebridge or aria() on download completion of aria
