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
import time # for mess()


def pluses(): # TODO debug
    for r in d['repos']: # out of pushsite() TODO only pull spinala here rest perhaps in a complete back up funktion
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git", True) # TODO move this to setup function
        print(f"cloned {r} to {os.path.join(d['puthere'], 'reposetories')}")
    
    sub(f"plutil -convert xml1 -o {os.path.join(d['puthere'], 'reposetories', 'ff', 'SafariBookmarks.xml')} {os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')}", True) # out of parsereadlist() TODO move this to setup function

    # TODO review new message system and keep debuging especially aria
    # TODO implement in hb and backup config!!
    # TODO test if messages work when aria gets called via homebridge

def sub(cmdstring, waitforcompletion): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if waitforcompletion: return p.communicate()[0].decode() # this will wait for subprocess to finisih

def mess(message, title):
    sub(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")
    # TODO implement    sub("osascript -e 'tell app \"Terminal\"' -e ' do script \"qlmanage -p /Users/mini/Desktop/\"' -e 'set W to the id of window 1' -e 'set visible of window 1 to false' -e 'do script \"curl -s \\\"http://localhost:8080/motion?screen\\\" && exit \"' -e 'delay 2' -e 'close window id W' -e 'end tell'")
    # TODO implement    sub("osascript -e 'tell app \"Safari\"' -e 'open location \"https://crbyxwpzfl.github.io/spinala/\"' -e 'delay 2' -e 'close (current tab of window 1)' -e 'end tell'")
    # TODO implement    sub("osascript -e 'tell app \"System Events\"' -e 'keystroke space using {control down}' -e 'delay 0.5' -e 'keystroke the \"message\"' -e 'delay 0.5' -e 'keystroke space using {control down}' -e 'end tell'")
    # TODO implement    sub("osascript -e 'tell app \"Messages\"' -e 'activate' -e 'delay 1' -e 'end tell' -e 'tell application \"System Events\"' -e 'keystroke the \"https://crbyxwpzfl.github.io/spinala/\"' -e 'delay 1' -e 'keystroke return' -e 'delay 2' -e 'keystroke \"q\" using {command down}' -e 'end tell'", False)

def parsereadlist(): # when foldername not in downloaddir add url to aria or dlp dict
    plist = plistlib.load(open(os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist'), 'rb'))
    for child in plist['Children']:
        if child.get('Title', None) == 'com.apple.ReadingList':
            for item in child['Children']:
                foldername = (item['URIDictionary']['title'][:40] + item['URLString'][:40] + item['URLString'][-40:]).replace('/','-').replace(':','-').replace('.','-').replace(' ','-')
                if foldername not in os.listdir(d['puthere']) and not item['URLString'].startswith('https://'): d['ariaurls'].append([foldername, item['URLString']]) # all not https into aria
                if foldername not in os.listdir(d['puthere']) and item['URLString'].startswith('https://') and not item['URIDictionary']['title'].startswith('push vpn to '): d['dlpurls'].append([foldername, item['URLString']]) # all https and not vpn to into dlp
                if item['URIDictionary']['title'].startswith('push vpn to '): d['vpnto'] = "connect " + item['URLString'][-2:] # vpn to country into d 'vpnto'

def vpnstate(): # pipe vpn status into dict
    nicelist = sub(d['sshpi'] + "nordvpn status", True).lstrip('\r-\r  \r\r-\r  \r').rstrip('\n').split('\n') # get vpn status and clean up output a bit
    for count, elem in enumerate(nicelist): d[nicelist[count].split(': ')[0]] = nicelist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value to dict

def overwritesite(): # overwrite site content corrosponding to parsereadlist() not vpnstate()
    d['color'] = "#fc4444" if d.get('vpnto', "Disconnected") == "Disconnected" else "#5cf287" # get on off color insert color part of css class selector
    d['line52'] = f'window.onload = load( \"{d.get("vpnto", "off")[8:]}\", \"{d["color"]}\", {int(60/len(d.get("vpnto", "chars-to-divide-to-one-this-is-long--ha--thats-what-she-said")))} )\n' # pass site vpn loc and color and stroke width. css displays 'off' state just by color with css class selector, therefore germany has class 'de' and 'off' but js loads diferent icon for 'off' and 'de'
    d['line56'] = f'<meta property=\"og:image\" content=\"https://github.com/crbyxwpzfl/spinala/raw/main/locs/{d.get("vpnto", "off")[8:]}/trans-og.png\"/> <!-- imessage wont execute js so these musst be set via github push -->\n'
    for line in fileinput.input([os.path.join(d['puthere'], 'reposetories', 'spinala', 'index.html')], inplace=True): # open file and overwrite lines
        print(d['line52'], end='') if fileinput.filelineno() == 52 else print(d['line56'], end='') if fileinput.filelineno() == 56 else print(line, end='')

def pushsite(): # pull all repos and push changes of overwritesite()
    sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} pull", True) # TODO gets changes from remote add --quiet to shut up 
    overwritesite() # update site content
    sub(f"git -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} commit -am \"site update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} push ;", True) # commit -am does not picup on newly created files
    sub(f"osascript -e 'tell application \"Messages\" to send \"{d.get('vpnto', 'off')}\" to participant \"{d['phonenr']}\"'", False)
    sub("osascript -e 'tell app \"Messages\"' -e 'activate' -e 'delay 1' -e 'end tell' -e 'tell application \"System Events\"' -e 'keystroke the \"https://crbyxwpzfl.github.io/spinala/\"' -e 'delay 1' -e 'keystroke return' -e 'delay 3' -e 'keystroke \"q\" using {command down}' -e 'end tell'", False) # dont wait use this so link preview loads nicely

def dlp(): # TODO perhaps use internal merge/convert tool with ffmpeg to generate mp4 and use archive at d['puthere']/repos/ff/dwl-archive
    parsereadlist() # to get desired urls now in new process here head() and paresreadlist never got called
    for url in d['dlpurls']:
        d['dlpopts']['outtmpl'] = os.path.join(d['puthere'], url[0], 'filename-vc:%(vcodec)s-ac:%(acodec)s.%(ext)s') # the first item in each url list is the foldername
        with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(url[1]) # the second item in each url list is the url
        sub(f"osascript -e 'display notification \"done {url[1]}\" with title \"dlp\"'", False) # dont wait on completion just fire notification
    os.kill(os.getppid(), signal.SIGHUP) # close window when done

def sendaria(data):
        try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
        except requests.exceptions.ConnectionError: # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time
            if d['Status'] == "Connected": sub(f"aria2c {d['ariaopts']}", False) # dont until completion so aria does not stop script execution since daemon mode is false so completion hook works # if status connected is essential cause all calls of script without any argumt are running aria() this is cause arie completion hook passes gid as first argumetn so non static so not specifiabl in dict
            # TODO perhaps use this sub(f"osascript -e 'tell app \"Terminal\" to do script \"aria2c {d['ariaopts']}\" ' ", True))
            # TODO aria starts to fast so next url call fails so no d['r'] so key error

def aria(): # TODO perhaps use more advanced opts add trackers and optimize concurrent downloads and save savefile every sec or so
    for url in d['ariaurls']: # on download completion call or when aria on but no urls this bitsh empty so yeeet    smae for if not d['ariaurls'] at shutdown purge send message
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [url[1]], { 'dir': os.path.join(d['puthere'], url[0]) } ] } ) # send aria the url from lit url[1] and the dir with foldername from list url[0]
    sendaria( {'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[{'methodName':'aria2.getGlobalStat'}, {'methodName': 'aria2.tellStopped', 'params':[0,20,['status', 'files', 'errorMessage']]}]]} ) # retrive info of aria
    # TODO if no urls passed aria never gets called so never updates count here
    d['CurrentRelativeHumidity'] = int(json.loads(d['r'].content)['result'][0][0].get('numActive')) + int(json.loads(d['r'].content)['result'][0][0].get('numWaiting')) # all urls in aria
    for stopped in json.loads(d['r'].content)['result'][1][0]: # man im numb all this nested list dict shit braeks me here we want the first list in the second list in r content result list
        d['message'] = f"{stopped.get('status')} {stopped.get('errorMessage')[:80]}" # make message
        for fs in stopped.get('files', [{'path':'nofile'}]):
            d['message'] = f"{fs.get('path')} {d['message']}"
            if not d['ariaurls']: sub(f"osascript -e 'display notification \"{d['message']}\" with title \"aria\"'", False) # dont wait on completion just fire notification # only on aria completion call so when no parsing happend so ther is no d['ariaurls']
            # TODO remove if not d['ariaurls']: mess("tell app \"Terminal\"", f"-e 'do script \"echo {d['message']} echo && du -hs {d['puthere']}*\"' -e 'end tell'")
    if not d['ariaurls']: sendaria({'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.purgeDownloadResult'}) # TODO no purge to keep history of errors  purge aria so next message is clean shuld be save and shuld not make me miss anything
    if not d['ariaurls'] and d['CurrentRelativeHumidity'] == 0: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} ) #if no active and no waiting in queue shutdown aria 

def head():
    parsereadlist() # waht u want vpn location and urls
    vpnstate() # where u are
    if d.get('vpnto', "what u want wh")[-2:] != d.get('Current server', "where u are")[:2]: sub(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"), True) # only set vpn when parsereadlist() vpn state not current vpnstate()
    if d.get('vpnto', "what u want wh")[-2:] != d.get('Current server', "where u are")[:2]: pushsite() # only push site when parsereadlist() vpnstate not current vpnstate(). pushsite() itself sets site corrosponding to parsereadlist() not vpnstate()

    if len(sub("killall -s aria2c", True).split('kill')) == 2 and d.get('Uptime', 'shiiit') == "shiiit": # prolly should not happen but yeah
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} )
        sub(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'", True)

    if (d.get('vpnto', "what u want wh")[-2:] == d.get('Current server', "where u are")[:2] and d['Status'] == "Connected" and d['ariaurls']) or d['StatusActive'] == 1: # dont do aria() when parsereadlist()-vpn-state not vpnstate() or do aria if arria2c running for updating relhumidity
        aria()

    if d.get('vpnto', "what u want wh")[-2:] == d.get('Current server', "where u are")[:2] and d['Status'] == "Connected" and d['dlpurls'] and len(sub("killall -s Python", True).split('kill')) == 2:  # +1 account for list.split always len 1 and +1 for Python currently running so this means if no dlp is up
        sub(f"osascript -e 'tell app \"Terminal\" to do script \"{pathlib.Path(__file__).resolve()} dlp\" ' ", False) # dont wait until completion call itself and bring dlp() up in new window

    print(d.get(sys.argv[3].strip("''") , int(len(d.get('Uptime', ''))/len(d.get('Uptime', '1'))) )) # print aria count to homebridge or print aria on as 'StatusActive' or calculate vpn on as 'StatusTampered' as in location tampered
    sys.exit()

d = {'debug': pluses,'Get': head, 'dlp': dlp,# defs for running directly in cli via arguments
    'CurrentRelativeHumidity': 0, 'StatusActive': len(sub("killall -s aria2c", True).split('kill'))-1, # for homebridge
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned
    'puthere': '/Users/mini/Downloads/', # put d['puthere']/reposetories  d['puthere']/gists  d['puthere']/repos/ff/xmlbookmarks  here
    'message': " ", # message to send
    'phonenr': privates.phone,
    'ariaurls': [],
    'dlpurls': [],
    'dlpopts': {'simulate': False, 'restrict-filenames': False, 'ignoreerrors': True, 'format': 'bestvideo*,bestaudio', 'verbos': True, 'external_downloader': {'m3u8': 'aria2c'}},
    'ariaopts': f"--enable-rpc --rpc-listen-all --on-download-complete={pathlib.Path(__file__).resolve()} --save-session=/Users/mini/Desktop/ariasfile.txt --input-file=/Users/mini/Desktop/ariasfile.txt --daemon=false --auto-file-renaming=false --allow-overwrite=false --seed-time=0", # daemon false otherwise no message on completion reason unknown
}
d.get(sys.argv[1].strip("''"), aria)() # call head() with 'Get' from homebridge or aria() on download completion of aria only works daemon false remember to not wait for completion on aria start
