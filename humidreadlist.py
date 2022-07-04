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
import sqlite3 # for parsereadlist()
import requests # for currentloc()


def sub(cmdstring, waitforcompletion): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if waitforcompletion: return p.communicate()[0].decode() # this will wait for subprocess to finisih

def mess(message, title):
    sub(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")
    # TODO implement    sub("osascript -e 'tell app \"Terminal\"' -e ' do script \"qlmanage -p /Users/mini/Desktop/\"' -e 'set W to the id of window 1' -e 'set visible of window 1 to false' -e 'do script \"curl -s \\\"http://localhost:8080/motion?screen\\\" && exit \"' -e 'delay 2' -e 'close window id W' -e 'end tell'")
    # TODO implement    sub("osascript -e 'tell app \"Safari\"' -e 'open location \"https://crbyxwpzfl.github.io/spinala/\"' -e 'delay 2' -e 'close (current tab of window 1)' -e 'end tell'")
    # TODO implement    sub("osascript -e 'tell app \"System Events\"' -e 'keystroke space using {control down}' -e 'delay 0.5' -e 'keystroke the \"message\"' -e 'delay 0.5' -e 'keystroke space using {control down}' -e 'end tell'")
    # TODO implement    sub("osascript -e 'tell app \"Messages\"' -e 'activate' -e 'delay 1' -e 'end tell' -e 'tell application \"System Events\"' -e 'keystroke the \"https://crbyxwpzfl.github.io/spinala/\"' -e 'delay 1' -e 'keystroke return' -e 'delay 2' -e 'keystroke \"q\" using {command down}' -e 'end tell'", False)
    # TODO implement    sub("tell app \"Terminal\"", f"-e 'do script \"echo {d['message']} echo && du -hs {d['puthere']}*\"' -e 'end tell'")

def parsereadlist(): # when foldername not in downloaddir add url to aria or dlp dict
    listoftupls = sqlite3.connect(d['chatdb']).cursor().execute(d['sqlquery']).fetchall() # sql connect make cursor execute query wait for query to finish
    for tupl in listoftupls:
        if '??' in tupl[0] and tupl[0].rsplit('??',1)[1] not in os.listdir(os.path.join(d['puthere'], 'temps')) and tupl[0].startswith('https://'): d['dlpurls'].append(tupl[0].rsplit('??',1)) # all https into dlp
        if '??' in tupl[0] and tupl[0].rsplit('??',1)[1] not in os.listdir(os.path.join(d['puthere'], 'temps')) and tupl[0].startswith('http://'): d['ariaurls'].append(tupl[0].strip('http://').rsplit('??',1)) # all http into aria
        if tupl[0].startswith('to '): d['vpnto'] = "connect " + tupl[0][-2:]  # connect country code into d 'vpnto'

def currentloc(): # TODO atleast check response code here otherwise anything but de will be handled as if vpn is on
    d['currentloc'] = requests.get(f'http://ipinfo.io/country', timeout=2, verify=False).content.decode().strip().lower()', # here no https cause of error message
# TODO theoreticly outdated by ping ip
#def vpnstate(): # pipe vpn status into dict
#    nicelist = sub(d['sshpi'] + "nordvpn status", True).rstrip(); nicelist = nicelist[nicelist.index("Status"):].split('\n') # get vpn status and clean up output a bit works unless trailing tarsh is added to cmd output
#    for count, elem in enumerate(nicelist): d[nicelist[count].split(': ')[0]] = nicelist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value to dict

def overwritesite(): # overwrite site content corrosponding to parsereadlist() not vpnstate()
    d['color'] = "#fc4444" if d.get('vpnto', "Disconnected") == "Disconnected" else "#5cf287" # get on off color insert color part of css class selector
    d['line52'] = f'window.onload = load( \"{d.get("vpnto", "connect off")[8:]}\", \"{d["color"]}\", {int(60/len(d.get("vpnto", "chars-to-divide-to-one-this-is-long--ha--thats-what-she-said")))} )\n' # pass site vpn loc and color and stroke width. css displays 'off' state just by color with css class selector, therefore germany has class 'de' and 'off' but js loads diferent icon for 'off' and 'de'
    d['line56'] = f'<meta property=\"og:image\" content=\"https://github.com/crbyxwpzfl/spinala/raw/main/locs/{d.get("vpnto", "connect off")[8:]}/trans-og.png\"/> <!-- imessage wont execute js so these musst be set via github push -->\n'
    for line in fileinput.input([os.path.join(d['puthere'], 'transfer', 'reposetories', 'spinala', 'index.html')], inplace=True): # open file and overwrite lines
        print(d['line52'], end='') if fileinput.filelineno() == 52 else print(d['line56'], end='') if fileinput.filelineno() == 56 else print(line, end='')

def pushsite(): # pull all repos and push changes of overwritesite()
    sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'transfer','reposetories', 'spinala')} pull", True) # TODO gets changes from remote add --quiet to shut up 
    overwritesite() # update site content
    sub(f"git -C {os.path.join(d['puthere'], 'transfer', 'reposetories', 'spinala')} commit -am \"site update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'transfer', 'reposetories', 'spinala')} push ;", True) # commit -am does not picup on newly created files
    #sub(f"osascript -e 'tell application \"Messages\" to send \"{d.get('vpnto', 'connect off')}\" to participant \"{d['phonenr']}\"'", False)
    #sub("osascript -e 'tell app \"Messages\"' -e 'delay 120' -e 'activate' -e 'delay 1' -e 'end tell' -e 'tell application \"System Events\"' -e 'keystroke the \"https://crbyxwpzfl.github.io/spinala/\"' -e 'delay 1' -e 'keystroke return' -e 'delay 3' -e 'keystroke \"q\" using {command down}' -e 'end tell'", False) # first delay is so github already built the site with correct thubnail dont wait use this so link preview loads nicely

def dlp(): # TODO perhaps use internal merge/convert tool with ffmpeg to generate mp4 and use archive at d['puthere']/repos/ff/dwl-archive
    parsereadlist() # to get desired urls now in new process here head() and paresreadlist never got called
    for url in d['dlpurls']:
        d['dlpopts']['outtmpl'] = os.path.join(d['puthere'], 'temps', url[1], f"{url[1]}-%(title)s.%(ext)s") # the seccond item in each url list is the foldername
        with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(url[0]) # the first item in each url list is the url
        sub(f"osascript -e 'display notification \"done {url[1]}\" with title \"dlp\"'", True) # wait on completion for notification so on last run '&& exit' does not kill process until notification is out

def sendaria(data):
        try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
        except requests.exceptions.ConnectionError: # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time
            if d['currentloc'] != "de": sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"aria2c {d['ariaopts']} && exit\"' -e 'set miniaturized of window 1 to true' -e 'delay 1' -e 'end tell'", True) # open aria like this and wait delay so aria is propperly up before next request # if status connected is essential cause all calls of script without any argumt are running aria() this is cause arie completion hook passes gid as first argumetn so non static so not specifiabl in dict

def aria(): # TODO perhaps use more advanced opts add trackers and optimize concurrent downloads and save savefile every sec or so
    for url in d['ariaurls']: # on download completion call or when aria on but no urls this bitsh empty so yeeet    smae for if not d['ariaurls'] at shutdown purge send message
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [url[0]], { 'dir': os.path.join(d['puthere'], 'temps', url[1]) } ] } ) # send aria the url from list url[0] and the dir with foldername from list url[1]
    sendaria( {'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[{'methodName':'aria2.getGlobalStat'}, {'methodName': 'aria2.tellStopped', 'params':[0,20,['status', 'files', 'errorMessage']]}]]} ) # retrive info of aria
    for stopped in json.loads(d['r'].content)['result'][1][0]: # man im numb all this nested list dict shit braeks me here we want the first list in the second list in r content result list
        d['message'] = f"{stopped.get('status')} {stopped.get('errorMessage')[:80]}" # make message
        for fs in stopped.get('files', [{'path':'nofile'}]):
            d['message'] = f"{fs.get('path')} {d['message']}"
            if not d['ariaurls']: sub(f"osascript -e 'display notification \"{d['message']}\" with title \"aria\"'", False) # dont wait on completion just fire notification # only on aria completion call so when no parsing happend so ther is no d['ariaurls']
    if not d['ariaurls']: sendaria({'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.purgeDownloadResult'}) # TODO no purge to keep history of errors  purge aria so next message is clean shuld be save and shuld not make me miss anything
    if not d['ariaurls'] and (int(json.loads(d['r'].content)['result'][0][0].get('numActive')) + int(json.loads(d['r'].content)['result'][0][0].get('numWaiting'))) == 0: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} ) #if no active and no waiting in queue shutdown aria

def sort():
    #TODO sorting algorithm for aria dls

def interpreter():
    #TODO perhaps wirte an interpreter for message commands
    # TODO start stop parsec if d['parsecoff'] and sub("pgrep -lf .parsec", True): sub("killall parsecd", True) else sub("open /Applications/Parsec.app", True)
    # TODO make backup

def head(): # run full head just on 'StatusTampered' to minimize pi querries
    parsereadlist() # waht u want vpn location and urls
    currentloc() # where u are

    if d['currentloc'] == "de" and sub("pgrep -lf aria.", True): # prolly should not happen but yeah aria on but vpn off kill all
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} )
        sub(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'", True)

    if d['currentloc'] != d.get('vpnto', "connect de")[-2:]: sub(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"), True); pushsite() # TODO dont wait on sub to finish here! only set vpn when parsereadlist() vpn state not current vpnstate()

    # TODO theoreticly outdated via ip ping
    # if d.get('vpnto', "connect --")[-2:] != d.get('Current server', "--")[:2]: sub(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"), True) # only set vpn when parsereadlist() vpn state not current vpnstate()
    # if d.get('vpnto', "connect --")[-2:] != d.get('Current server', "--")[:2]: pushsite() # only push site when parsereadlist() vpnstate not current vpnstate(). pushsite() itself sets site corrosponding to parsereadlist() not vpnstate()
    # if  len(sub("killall -s aria2c", True).split('kill'))-1 == 1 and d.get('Uptime', 'shiiiit') == "shiiiit": # prolly should not happen but yeah aria on but vpn off
    #    sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} )
    #    sub(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'", True)

    # TODO why did aria not start on every run with or (len(sub("killall -s aria2c", True).split('kill'))-1 == 1)
    if d['currentloc'] != d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['ariaurls']: # dont do aria() when parsereadlist()-vpn-state not vpnstate() or do aria if arria2c running for updating relhumidity
        aria()

    if d['currentloc'] != d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['dlpurls'] and not sub("pgrep -lf .dlp", True):  # and not dlp currently running then do dlp()
        sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"{pathlib.Path(__file__).resolve()} dlp && exit\"' -e 'set miniaturized of window 1 to true' -e 'end tell'", False) # dont wait until completion call itself and bring dlp() up in new window

    print(d.get(sys.argv[3].strip("''"), len(d['ariaurls']) + len(['dlpurls']) )) # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge
d = {'Get': head, 'dlp': dlp, # defs for running directly in cli via arguments
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'puthere': '/Users/mini/Downloads/', # put 'puthere'/transfer/reposetories/spinala for site update and 'puthere'/temps/dwls here
    'phonenr': privates.phone, # for vpn message and sql query
    'ariaurls': [],
    'dlpurls': [],
    'dlpopts':{'simulate': False, 'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'restrict-filenames': False, 'ignoreerrors': True, 'verbos': True},
    'ariaopts': f"--enable-rpc --rpc-listen-all --on-download-complete={pathlib.Path(__file__).resolve()} --save-session=/Users/mini/Desktop/ariasfile.txt --input-file=/Users/mini/Desktop/ariasfile.txt --daemon=false --auto-file-renaming=false --allow-overwrite=false --seed-time=0", # daemon false otherwise no message on completion reason unknown
    'chatdb': '/Users/mini/Library/Messages/chat.db',
    'sqlquery': f'SELECT message.text FROM message JOIN chat_handle_join ON message.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id WHERE (chat.chat_identifier="{privates.mail}" OR chat.chat_identifier="{privates.phone}") ORDER BY message.date desc;'
}
d.get(sys.argv[1].strip("''"), aria)() # call head() with 'Get' from homebridge or aria() on download completion of aria only works daemon false remember to not wait for completion on aria start
