#!/usr/bin/env python3
#chmod +x /current/file


#let the cluster fuck begin


import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
import os
import subprocess
#import plistlib # for parsereadlist()
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

def parsereadlist(): # when foldername not in downloaddir add url to aria or dlp dict
    d['sqlquery'] = f'SELECT message.text, message.date FROM message JOIN chat_handle_join ON message.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id WHERE (chat.chat_identifier="{privates.mail}" OR chat.chat_identifier="{privates.phone}") ORDER BY message.date desc;'
    listoftupls = sqlite3.connect(d['chatdb']).cursor().execute(d['sqlquery']).fetchall() # sql connect make cursor execute query wait for query to finish
    for tupl in listoftupls:
        if tupl[0].startswith('https://') and str(tupl[1]) not in os.listdir(os.path.join(d['puthere'], 'temps')): d['dlpurls'].append( list(map(str,tupl)) ) # all https into dlp
        if tupl[0].startswith('http://') and tupl[0].strip('http://').split('?',1)[0] not in os.listdir(os.path.join(d['puthere'], 'temps')): d['ariaurls'].append(tupl[0].strip('http://').split('?',1)) # all http into aria split on first ? so naming convention is http://filename?...
        if tupl[0].startswith('to '): d['vpnto'] = "connect " + tupl[0][-2:]  # connect country code into d 'vpnto'

def currentloc():
    d['currentloc'] = requests.get(f'http://ipinfo.io/json', timeout=2, verify=False).json().get('country', "DE").lower() # TODO everything but de will be treated as vpn on this is very bad here no https cause of error message

def dlp(): # TODO perhaps use archive at d['puthere']/repos/ff/dwl-archive
    d['dlpopts']['outtmpl'] = os.path.join(d['puthere'], 'temps', sys.argv[3], f"{sys.argv[3]}-%(title)s.%(ext)s") # the seccond sys arg in each dlp call is the foldername
    with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(sys.argv[2]) # the first sys arg in each dlp call is the url
    sub(f"osascript -e 'display notification \"done {sys.argv[3]}\" with title \"dlp\"'", True) # wait on completion for notification so on last run '&& exit' does not kill process until notification is out

def sendaria(data):
        try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
        except requests.exceptions.ConnectionError: # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time
            if d['currentloc'] != "de": sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"aria2c {d['ariaopts']} && exit\"' -e 'set miniaturized of window 1 to true' -e 'delay 1' -e 'end tell'", True) # open aria like this and wait delay so aria is propperly up before next request # if status connected is essential cause all calls of script without any argumt are running ariahead() this is cause arie completion hook passes gid as first argumetn so non static so not specifiable in dict

def ariainfo(): # TODO longterm rework the message handling
    sendaria( {'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[{'methodName':'aria2.getGlobalStat'}, {'methodName': 'aria2.tellStopped', 'params':[0,20,['status', 'files', 'errorMessage']]}]]} ) # retrive info of aria
    for stopped in json.loads(d['r'].content)['result'][1][0]: # man im numb all this nested list dict shit braeks me here we want the first list in the second list in r content result list
        d['message'] = f"{stopped.get('status')} {stopped.get('errorMessage')[:80]}" # make message
        for fs in stopped.get('files', [{'path':'nofile'}]):
            d['message'] = f"{fs.get('path')} {d['message']}"
            sub(f"osascript -e 'display notification \"{d['message']}\" with title \"aria\"'", False) # dont wait on completion just fire notification # only on aria completion call so when no parsing happend so ther is no d['ariaurls']

def ariacleanup():
    # TODO logterm remove url wich are not any longer in dlpurls as a way to cancle downloads
    if (int(json.loads(d['r'].content)['result'][0][0].get('numActive')) + int(json.loads(d['r'].content)['result'][0][0].get('numWaiting'))) == 0: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} ) #if no active and no waiting in queue shutdown aria
    else: sendaria({'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.purgeDownloadResult'}) # TODO no purge to keep history of errors  purge aria so next message is clean shuld be save and shuld not make me miss anything

def ariasort(finalfile):
    d = {'puthere': '/Users/mini/Downloads/'}
    # TODO perhaps include nested folders into filenaming
    for path, subdirs, files in os.walk(os.path.join(d['puthere'], 'temps', finalfile)):
        for name in [f for f in files if f.endswith(".srt")]: # this selects the most nested subt.srt when not set ffmpeg sub() just uses -map 0 to copy all subs when present
            d['includesubs'] = f' -i \"{str(os.path.join(path, name))}\"'
        for name in [f for f in files if f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".avi")]: # this selects all avis mkvs mp4s and renames or (down) remuxes them to mp4
            print(f"ffmpeg -n -i \"{str(os.path.join(path, name))}\" {d.get('includesubs', "-map 0")} -metadata title= -vcodec copy -acodec copy -scodec \"mov_text\" -ac 8 \"{d.get('iter',"")}{str(os.path.join(path, finalfile))}.mp4\"", True)
            d['iter'] = d.get('iter',0) + 1 # for more files in same folder iter gets set and ffmpeg sub() puts iteration infront of file sarting with 1

sysargv3 = "/Users/mini/Downloads/temps/uncharted-small/Uncharted.2022.HDRip.XviD.AC3-EVO.avi"
ariasort(sysargv3.split('/')[len(os.path.join(d['puthere'], 'temps').split('/'))] if sysargv3 else None)


def ariahead(): # TODO perhaps use more advanced opts add trackers and optimize concurrent downloads and save savefile every sec or so
    for url in d['ariaurls']: # on download completion call this bitsh empty so yeeet    smae for no d['ariaurls'] at shutdown purge send message
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [url[1]], { 'dir': os.path.join(d['puthere'], 'temps', url[0]) } ] } ) # send aria the url from list url[1] and the dir with foldername from list url[0]
    if not d['ariaurls']: ariainfo() # just on completion call so no paresreadlist so no d['ariaurls']
    if not d['ariaurls']: ariacleanup() # just on completion call so no paresreadlist so no d['ariaurls']
    if not d['ariaurls']: ariasort( sys.argv[3].split('/')[len(os.path.join(d['puthere'], 'temps').split('/'))] if sys.argv[3] else None ) # just on completion call so no paresreadlist so no d['ariaurls']

def interpreter():
    #TODO perhaps wirte an interpreter for message commands
    # TODO start stop parsec if d['parsecoff'] and sub("pgrep -lf .parsec", True): sub("killall parsecd", True) else sub("open /Applications/Parsec.app", True)
    # TODO make backup

def head(): # run full head just on 'CurrentRelativeHumidity' to minimize pi querries
    parsereadlist() # waht u want vpn location and urls
    currentloc() # where u are

    if d['currentloc'] == "de" and sub("pgrep -lf aria.", True): # savety prolly should not happen but yeah aria on but vpn off kill all
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} )
        sub(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'", True)

    if d['currentloc'] != d.get('vpnto', "connect de")[-2:]: sub(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"), True); # TODO dont wait on sub to finish here! only set vpn when parsereadlist() vpn state not current vpnstate()

    # TODO why did aria not start on every run with or (len(sub("killall -s aria2c", True).split('kill'))-1 == 1)
    if d['currentloc'] == d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['ariaurls']: # dont do aria() when parsereadlist()-vpn-state not vpnstate()
        ariahead()

    if d['currentloc'] == d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['dlpurls'] and not sub("pgrep -lf .dlp", True): # not dlp currently running then do dlp()
        sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"mkdir -p {os.path.join(d['puthere'], 'temps', d['dlpurls'][0][1])} && {pathlib.Path(__file__).resolve()} dlp \\\"{d['dlpurls'][0][0]}\\\" {d['dlpurls'][0][1]} &> {os.path.join(d['puthere'], 'temps', d['dlpurls'][0][1], 'log.txt')} && exit\"' -e 'set miniaturized of window 1 to true' -e 'end tell'", False) # dont wait until completion call itself and bring dlp() up for one url in new window

    print(d.get(sys.argv[3].strip("''"), len(d['ariaurls']) + len(d['dlpurls']) )) # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge

d = {'Get': head, 'dlp': dlp, # defs for running directly in cli via arguments
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'puthere': '/Users/mini/Downloads/', # put 'puthere'/transfer/reposetories/spinala for site update and 'puthere'/temps/dwls here
    'phonenr': privates.phone, # for vpn message and sql query
    'ariaurls': [],
    'dlpurls': [],
    'dlpopts':{'verbose': True, 'simulate': False, 'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'restrict-filenames': False, 'ignoreerrors': True, 'verbos': True},
    'ariaopts': f"--enable-rpc --rpc-listen-all --on-download-complete={pathlib.Path(__file__).resolve()} --save-session=/Users/mini/Desktop/ariasfile.txt --input-file=/Users/mini/Desktop/ariasfile.txt --daemon=false --auto-file-renaming=false --allow-overwrite=false --seed-time=0", # daemon false otherwise no message on completion reason unknown
    'chatdb': '/Users/mini/Library/Messages/chat.db'
}
d.get(sys.argv[1].strip("''"), ariahead)() # call head() with 'Get' from homebridge or ariahead() on download completion of aria only works daemon false remember to not wait for completion on aria start
