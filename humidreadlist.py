#!/usr/bin/env python3
# chmod +x /current/file && cd "/current/" && git config core.filemode true && git commit -am "commit chmodx" && git -c core.sshCommand="ssh -i /path/to/priv" push


#let the cluster fuck begin



import sys; sys.path.append('/Users/mini/Downloads/transfer/reps-privates/'); import secs  # fetch secrets

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
    d['sqlquery'] = f'SELECT message.text, message.date FROM message JOIN chat_handle_join ON message.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id LEFT JOIN chat_recoverable_message_join ON chat_recoverable_message_join.message_id = message.ROWID WHERE message.associated_message_type = 0 AND (chat.chat_identifier="{secs.mail}" OR chat.chat_identifier="{secs.phone}") AND message.is_from_me = 0 AND chat_recoverable_message_join.message_id IS NULL ORDER BY message.date desc; '
    # TODO find out where edited or 2min deleted messages go

    # add all messages with !! to list for tapback() 
        # NOTE MAKE ABOLUTLY SURE deleted messages dont stay in here cause eg -> vpn turns off every time there is a tapback['vpn to': !!]
        # NOTE so deleted messages dont stick in list

    # sth is already handled is no longer determind by folder exists but tapback status
    # when sth is done it will be marked with thumbs up -> eclude from list
    # when sth is error it will be marked with ? -> eclude from list
    # when sth is active it will be marked with thumbs down -> exclude from list
    # when sth is toberemoved it will be marked with !! -> exlude from list
        # NOTE this means all tapback() need to run in same proces (cant be dispatched) 
        # NOTE so tapbacks cant lack behind since what to do relies detects based on tapback status 
        # NOTE this gets problematic for a lot of tapbacks in one run (eg set vpn and delete a bunch off messages)

    listoftupls = sqlite3.connect(d['chatdb']).cursor().execute(d['sqlquery']).fetchall()  # sql connect make cursor execute query wait for query to finish
    for tupl in listoftupls:
        if tupl[0].startswith('https://') and str(tupl[1]) not in os.listdir(os.path.join(d['puthere'], 'temps')): d['dlpurls'].append( list(map(str,tupl)) )  # all https into dlp
        if tupl[0].startswith('http://') and tupl[0].replace('http://', '').split('/',1)[0] not in os.listdir(os.path.join(d['puthere'], 'temps')): d['ariaurls'].append(tupl[0].replace('http://', '').split('/',1))  # all http into aria split on first / after http:// strip so naming convention is http://filename/...
        if tupl[0].startswith('http://'): d['allariaurls'].append(tupl[0].replace('http://', '').split('/',1))  # all aria urls present in messages to check against for removal in arai cleanup
        if tupl[0].startswith('to '): d['vpnto'] = "connect " + tupl[0][-2:]  # connect country code into d 'vpnto'

def currentloc():
    d['currentloc'] = requests.get(f'http://ipinfo.io/json', timeout=2, verify=False).json().get('country', "DE").lower()  # everything but de will be treated as vpn on this is very bad here no https cause of error message

def dlp():  # perhaps use archive at d['puthere']/repos/ff/dwl-archive
    # dlp rewrite TODO just get extracted url from dlp and pass url into aria to get completion, active, error updates
        # then mark folder for sort() so audio gets extracted
        # handle error case when dlp cant get url

    # this still prints ERROR: unsupported URL to stdout/stderr
    try: import yt_dlp; print(yt_dlp.YoutubeDL({'no_warnings': True, 'quiet': True, 'format_sort': ['ext'],'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'restrict-filenames': False, 'ignoreerrors': True, }).extract_info(URLS, download=False)['format_id']) # cant use this to just extract url since aria does not support hls 'format_id' to verify selection 
    except (yt_dlp.utils.UnsupportedError, yt_dlp.utils.DownloadError): print("error")


    d['dlpopts'] = {'verbose': True, 'simulate': False, 'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'restrict-filenames': False, 'ignoreerrors': True, 'verbos': True}
    d['dlpopts']['outtmpl'] = os.path.join(d['puthere'], 'temps', sys.argv[3], f"%(title)s-{sys.argv[3]}.%(ext)s")  # the seccond sys arg in each dlp call is the foldername
    with yt_dlp.YoutubeDL(d['dlpopts']) as ydl: ydl.download(sys.argv[2])  # the first sys arg in each dlp call is the url
    # [ ] TODO find a way to detect active dl of dlp -> put actives in tapbacklist[(message , thumbs down), ...]
    # [ ] TODO find a way to cancle active dlp wich are in tapback[] and have value !! AND deleted messages (if they are not in list already)
    # [ ] TODO find a way to detect error of dlp -> update errors in tapback['message': ?, ...]
    # [ ] TODO find a way to detect complete dl -> put in tapback['message': thumbsup]
        # all detections maby possible via spawning dlp as server like aria responding to questions ????

def sendaria(data):  # sends json to aria or starts aria if aria not reachable
    try: d['r'] = requests.post('http://localhost:6800/jsonrpc', json=data, verify=False, timeout=2)
    except requests.exceptions.ConnectionError: # error connecting so aria is off so start aria so no added url so url stays in queue so addes url next time
        d['ariaopts'] = f"--enable-rpc --rpc-listen-all --on-download-complete={pathlib.Path(__file__).resolve()} --save-session={os.path.join(d['puthere'], 'temps', 'ariasfile.txt')} --input-file={os.path.join(d['puthere'], 'temps', 'ariasfile.txt')} --daemon=false --auto-file-renaming=false --allow-overwrite=false --seed-time=0" # daemon false otherwise no message on completion reason unknown but not to bad so one sees whats happening
        sub(f"screen -S aria -d -m aria2c {d['ariaopts']}", False)  # open aria like this no wait cause next call in 60sec wait delay so aria is propperly up before next request  status connected check is not essential cause #TODO why we have completion call!! no completioncall any more

def ariacleanup():  # perhaps to clean memory  else: sendaria({'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.purgeDownloadResult'}) #  purge aria so aria save file is celan
    sendaria({ 'jsonrpc':'2.0', 'id':'mini', 'method':'system.multicall', 'params':[[ {'methodName':'aria2.getGlobalStat'}, {'methodName':'aria2.tellStopped', 'params':[0,20,['status', 'gid', 'dir']]}, {'methodName':'aria2.tellWaiting', 'params':[0,20,['status', 'gid', 'dir']]}, {'methodName':'aria2.tellActive', 'params':[['status', 'gid', 'dir']]} ]] })  
    if (len(d['ariaurls']) + int(json.loads(d['r'].content)['result'][0][0].get('numActive')) + int(json.loads(d['r'].content)['result'][0][0].get('numWaiting'))) == 0: sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.shutdown'} ); sys.exit()  # no ariaurls no active no waiting shutdown aria and sys exit otherwise for loop benethe will throw error list index out of range since no actives
    for actives in json.loads(d['r'].content)['result'][3][0]:
        if not any(actives.get('dir').split('/')[len(os.path.join(d['puthere'], 'temps').split('/'))] in sublist for sublist in d['allariaurls']): sendaria({ 'jsonrpc':'2.0', 'id':'mini', 'method':'aria2.remove', 'params':[actives.get('gid')] })
    # TODO put all actives or waiting in tapback[ 'message': thumbs down]
    # TODO throw out all actives wich are in tapbackdict with value !! AND deleted messages (if they are not in list already)
    # TODO put all errors in tapback['message': ?]
    # TODO put all complete tapback['message': tuhmbsup]

def sortaria(): #TODO rewrite to sortall()  #with /humidreadlist.py palce holder /path/to/file.mkv you manually pass to ariasort    perhaps include nested folders into filenaming  runns on completioncall of aria takes filedir from completioncall arguments
    d['finalfile'] = sys.argv[3].split('/')[len(os.path.join(d['puthere'], 'temps').split('/'))] if sys.argv[3] else sys.exit()  # sort files or exit when no files passed
    for path, subdirs, files in os.walk(os.path.join(d['puthere'], 'temps', d['finalfile'])):
        for name in [f for f in files if f.endswith(".srt") and f.lower().startswith("eng")]:  # this selects the most nested subt.srt when not set ffmpeg sub() just uses -map 0 to copy all subs of og file when present
            d['includesubs'] = f' -i \"{str(os.path.join(path, name))}\"'
    for path, subdirs, files in os.walk(os.path.join(d['puthere'], 'temps', d['finalfile'])):
        for name in sorted([f for f in files if f.endswith(".mp4") or f.endswith(".mkv") or f.endswith(".avi")]): # this selects all avis mkvs mp4s and renames or (down) remuxes them to mp4 in sorted order
            sub(f"ffmpeg -n -i \"{str(os.path.join(path, name))}\" {d.get('includesubs', '-map 0')} -metadata title= -vcodec copy -acodec copy -scodec \"mov_text\" -ac 8 \"{str(os.path.join(path, str(d.get('iter','')) + ' ' + d['finalfile'].replace('-', ' ') ))}.mp4\"", True)
            d['iter'] = d.get('iter',0) + 1  # for more files in same folder iter gets set and ffmpeg sub() puts iteration infront of file sarting with 1
    # TODO parse puthere folder convert all not alreadyconverted in seperate process
    # TODO update sort to auto put in bin (30d deletion!)


    # dlp rewrite TODO extract audio from dlp downloads perhaps markfolder with dlp

def tapback():
    # take dict of kind ['message text': tapback nr, ...] -> tapback accordingly on after on other
        # delete all items of list with tapback !! -> esential to clear out all tapback[] items with value !! especially for vpn off these must be gone on next run
        # NOTE messages taged with !! form mini mean this is a old message its deleted and not looked at agian

def head(): # run full head just on 'CurrentRelativeHumidity' to minimize pi querries
    parsereadlist() # waht u want vpn location and urls
    currentloc() # where u are

    if d['currentloc'] == "de" and sub("pgrep -lf aria.", True): # savety prolly should not happen but yeah aria on but vpn off kill all
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.forceShutdown'} )
        sub(f"osascript -e 'tell application \"Messages\" to send \"aria on vpn off\" to participant \"{d['phonenr']}\"'", True)

    if d['currentloc'] != d.get('vpnto', "connect de")[-2:]: 
        sub(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"), True);  # only set vpn when parsereadlist() vpn state not current vpnstate() this sometimes waits long for sub completion but dont feel good witch just a dispatch here
        # TODO perhaps just dispatch setvpn call to save runtime
        # TODO when dispatched vpn is running add to tapback['vpn to': thumbs down]
        # TODO when dispatched vpn not running check for vpn ok -> add to tapback['vpn to', thumbs up]
        # TODO vpn off would mean to check tapback[] for message with vpn to and value !!
        # TODO detect vpn error and add to tapback['vpn to': ?]

    if sub("pgrep -lf aria.", True):  # when aria is up
        ariacleanup()  # removes ariaurls and stops aria when no active or waiting

    if d['currentloc'] == d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['ariaurls']: # dont do aria() when parsereadlist()-vpn-state not vpnstate()
        sendaria( {'jsonrpc': '2.0', 'id': 'mini', 'method': 'aria2.addUri','params':[ [d['ariaurls'][0][1]], { 'dir': os.path.join(d['puthere'], 'temps', d['ariaurls'][0][0]) } ] } )  # send aria the first url[1] dir[0] pair from ariaurls list  perhaps use more advanced opts add trackers and optimize concurrent downloads and save savefile every sec or so

    if d['currentloc'] == d.get('vpnto', "connect de")[-2:] and d['currentloc'] != "de" and d['dlpurls'] and not sub("pgrep -lf .dlp", True): # not dlp currently running then do dlp()
        sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"mkdir -p {os.path.join(d['puthere'], 'temps', d['dlpurls'][0][1])} && {pathlib.Path(__file__).resolve()} dlp \\\"{d['dlpurls'][0][0]}\\\" {d['dlpurls'][0][1]} &> {os.path.join(d['puthere'], 'temps', d['dlpurls'][0][1], 'log.txt')} ; exit\"' -e 'set miniaturized of window 1 to false' -e 'end tell'", False) # dont wait until completion call itself and bring dlp() up for one url in new window

    print(d.get(sys.argv[3].strip("''"), len(d['ariaurls']) + len(d['dlpurls']) )) # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge

# TODO perhaps change temps to desktop dir

d = {'get': head, 'dlp': dlp, # defs for running directly in cli via arguments
    'sshpi': f"ssh spinala@192.168.2.1 -i {secs.minisshpriv} ", # attentione to the last space
    'puthere': '/Users/mini/Downloads/', # put 'puthere'/transfer/reposetories/spinala for site update and 'puthere'/temps/dwls here
    'phonenr': secs.phone, # for vpn message and sql query
    'ariaurls': [], 'allariaurls': [['list', 'notempty']], 'dlpurls': [],
    'chatdb': '/Users/mini/Library/Messages/chat.db'
}

d.get(sys.argv[1].strip("''").lower(), sortaria)()  # call head() with 'Get' from homebridge or ariasort() on download completion of aria  only works daemon false remember to not wait for completion on aria start
