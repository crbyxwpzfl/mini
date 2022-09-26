#r/bin/env python3
#chzmod +x /current/file


#let the cluster fuck begin



import sys; sys.path.append('/Users/mini/Downloads/transfer/reps/privates/'); import secs  # fetch secrets

import os
import subprocess
import pathlib  # for calling itself in dlp()
import yt_dlp  # for dlp()
import requests  # for aria() rpc interface
import json  # for aria()
import sqlite3  # for parsereadlist()
import requests  # for currentloc()


def sub(cmdstring, waitforcompletion):  # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if waitforcompletion: return p.communicate()[0].decode() # this will wait for subprocess to finisih

def parsereadlist():  # when foldername not in downloaddir add url to aria or dlp dict
    d['sqlquery'] = f'SELECT message.text, message.date FROM message JOIN chat_handle_join ON message.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id WHERE (chat.chat_identifier="{secs.mail}" OR chat.chat_identifier="{secs.phone}") ORDER BY message.date desc;'
    listoftupls = sqlite3.connect(d['chatdb']).cursor().execute(d['sqlquery']).fetchall()  # sql connect make cursor execute query wait for query to finish
    for tupl in listoftupls:
        if tupl[0].startswith('https://') and str(tupl[1]) not in os.listdir(os.path.join(d['puthere'], 'temps')): d['dlpurls'].append( list(map(str,tupl)) )  # all https into dlp
        if tupl[0].startswith('http://') and tupl[0].replace('http://', '').split('/',1)[0] not in os.listdir(os.path.join(d['puthere'], 'temps')): d['ariaurls'].append(tupl[0].replace('http://', '').split('/',1))  # all http into aria split on first / after http:// strip so naming convention is http://filename/...
        if tupl[0].startswith('http://'): d['allariaurls'].append(tupl[0].replace('http://', '').split('/',1))  # all aria urls present in messages to check against for removal in arai cleanup
        if tupl[0].startswith('to '): d['vpnto'] = "connect " + tupl[0][-2:]  # connect country code into d 'vpnto'

def currentloc():
    d['currentloc'] = requests.get(f'http://ipinfo.io/json', timeout=2, verify=False).json().get('country', "DE").lower()  # everything but de will be treated as vpn on this is very bad here no https cause of error message

def dlp():  # perhaps use archive at d['puthere']/repos/ff/dwl-archive
    d['dlpopts'] = {'verbose': True, 'simulate': False, 'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'restrict-filenames': False, 'ignoreerrors': True, 'verbos': True}
    d['dlpopts']['outtmpl'] = os.path.join(d['puthere'], 'temps', sys.argv[3], f"%(title)s-{sys.argv[3]}.%(ext)s")  # the seccond sys arg in each dlp call is the foldername
    with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(sys.argv[2])  # the first sys arg in each dlp call is the url

def sendaria(data):  # sends json to aria or starts aria if aria not reachable
    try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
    except requests.exceptions.ConnectionError: # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time
        d['ariaopts'] = f"--enable-rpc --rpc-listen-all --on-download-complete={pathlib.Path(__file__).resolve()} --save-session={os.path.join(d['puthere'], 'temps', 'ariasfile.txt')} --input-file={os.path.join(d['puthere'], 'temps', 'ariasfile.txt')} --daemon=false --auto-file-renaming=false --allow-overwrite=false --seed-time=0" # daemon false otherwise no message on completion reason unknown but not to bad so one sees whats happening
        sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"aria2c {d['ariaopts']} && exit\"' -e 'set miniaturized of window 1 to false' -e 'delay 1' -e 'end tell'", True)  # open aria like this and wait delay so aria is propperly up before next request  status connected check is not essential cause no completioncall any more

def ariacleanup():   # perhaps to clean memory  else: sendaria({'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.purgeDownloadResult'}) #  purge aria so aria save file is celan
    sendaria({ 'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[ {'methodName':'aria2.getGlobalStat'}, {'methodName':'aria2.tellStopped', 'params':[0,20,['status', 'gid', 'dir']]}, {'methodName':'aria2.tellWaiting', 'params':[0,20,['status', 'gid', 'dir']]}, {'methodName':'aria2.tellActive', 'params':[['status', 'gid', 'dir']]} ]] })  
    if (len(d['ariaurls']) + int(json.loads(d['r'].content)['result'][0][0].get('numActive')) + int(json.loads(d['r'].content)['result'][0][0].get('numWaiting'))) == 0: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} ); sys.exit()  # no ariaurls no active no waiting shutdown aria and sys exit otherwise for loop benethe will throw error list index out of range since no actives
    for actives in json.loads(d['r'].content)['result'][3][0]:
        if not any(actives.get('dir').split('/')[len(os.path.join(d['puthere'], 'temps').split('/'))] in sublist for sublist in d['allariaurls']): sendaria({ 'jsonrpc':'2.0', 'id':'mini', 'method':'aria2.remove', 'params':[actives.get('gid')] })
            
def sortaria():  # perhaps include nested folders into filenaming  runns on completioncall of aria takes filedir from completioncall arguments
    d['finalfile'] = sys.argv[3].split('/')[len(os.path.join(d['puthere'], 'temps').split('/'))] if sys.argv[3] else sys.exit()  # sort files or exit when no files passed
    for path, subdirs, files in os.walk(os.path.join(d['puthere'], 'temps', d['finalfile'])):
        for name in [f for f in files if f.endswith(".srt") and f.lower().startswith("eng")]:  # this selects the most nested subt.srt when not set ffmpeg sub() just uses -map 0 to copy all subs of og file when present
            d['includesubs'] = f' -i \"{str(os.path.join(path, name))}\"'
    for path, subdirs, files in os.walk(os.path.join(d['puthere'], 'temps', d['finalfile'])):
        for name in [f for f in files if f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".avi")]: # this selects all avis mkvs mp4s and renames or (down) remuxes them to mp4
            sub(f"ffmpeg -n -i \"{str(os.path.join(path, name))}\" {d.get('includesubs', '-map 0')} -metadata title= -vcodec copy -acodec copy -scodec \"mov_text\" -ac 8 \"{str(os.path.join(path, str(d.get('iter','')) + ' ' + d['finalfile'].replace('-', ' ') ))}.mp4\"", True)
            d['iter'] = d.get('iter',0) + 1  # for more files in same folder iter gets set and ffmpeg sub() puts iteration infront of file sarting with 1

def interpreter():
    #TODO perhaps wirte an interpreter for message commands
    # TODO start stop parsec if d['parsecoff'] and sub("pgrep -lf .parsec", True): sub("killall parsecd", True) else sub("open /Applications/Parsec.app", True)
    # TODO make backup
    print("todo")

def head(): # run full head just on 'CurrentRelativeHumidity' to minimize pi querries
    parsereadlist() # waht u want vpn location and urls
    currentloc() # where u are

    if d['currentloc'] == "de" and sub("pgrep -lf aria.", True): # savety prolly should not happen but yeah aria on but vpn off kill all
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.forceShutdown'} )
        sub(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'", True)

    if d['currentloc'] != d.get('vpnto', "connect de")[-2:]: 
        sub(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"), True);  # only set vpn when parsereadlist() vpn state not current vpnstate() this sometimes waits long for sub completion but dont feel good witch just a dispatch here

    if sub("pgrep -lf aria.", True):  # when aria is up
        ariacleanup()  # removes ariaurls and stops aria when no active or waiting

    if d['currentloc'] == d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['ariaurls']: # dont do aria() when parsereadlist()-vpn-state not vpnstate()
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [d['ariaurls'][0][1]], { 'dir': os.path.join(d['puthere'], 'temps', d['ariaurls'][0][0]) } ] } )  # send aria the first url[1] dir[0] pair from ariaurls list  perhaps use more advanced opts add trackers and optimize concurrent downloads and save savefile every sec or so

    if d['currentloc'] == d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['dlpurls'] and not sub("pgrep -lf .dlp", True): # not dlp currently running then do dlp()
        sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"mkdir -p {os.path.join(d['puthere'], 'temps', d['dlpurls'][0][1])} && {pathlib.Path(__file__).resolve()} dlp \\\"{d['dlpurls'][0][0]}\\\" {d['dlpurls'][0][1]} &> {os.path.join(d['puthere'], 'temps', d['dlpurls'][0][1], 'log.txt')} ; exit\"' -e 'set miniaturized of window 1 to false' -e 'end tell'", False) # dont wait until completion call itself and bring dlp() up for one url in new window

    print(d.get(sys.argv[3].strip("''"), len(d['ariaurls']) + len(d['dlpurls']) )) # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge

d = {'get': head, 'dlp': dlp, # defs for running directly in cli via arguments
    'sshpi': f"ssh spinala@192.168.2.1 -i {secs.minisshpriv} ", # attentione to the last space
    'puthere': '/Users/mini/Downloads/', # put 'puthere'/transfer/reposetories/spinala for site update and 'puthere'/temps/dwls here
    'phonenr': secs.phone, # for vpn message and sql query
    'ariaurls': [], 'allariaurls': [['list', 'notempty']], 'dlpurls': [],
    'chatdb': '/Users/mini/Library/Messages/chat.db'
}

d.get(sys.argv[1].strip("''").lower(), sortaria)()  # call head() with 'Get' from homebridge or ariasort() on download completion of aria  only works daemon false remember to not wait for completion on aria start
