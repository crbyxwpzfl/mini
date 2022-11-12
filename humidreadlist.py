#!/usr/bin/env python3
# chmod +x /current/file && cd "/current/" && git config core.filemode true && git commit -am "commit chmodx" && git -c core.sshCommand="ssh -i /path/to/priv" push


#let cluster fuck begin


# currently best idea
#
# vllt screen set vpn too and vllt screen tapbacks too
# differentiate aria and dlp screens launche new dlps but not arias
#
# shut off all dlp and aria screens when vpn is off
#
# find a good way to name screens use message date only as addon to uniquefy the name
#
# needs solid way to find active screens
# needs to alway end screen on fail or finished dl
# needs solid way to search dir for succesfull dl
#
# each call handles one message with !!
#
# if message with !! has screen delete/drop screen
# take message tapback !! and delete message
#
# check for vpn and how many screens are active i ok
#   spawn screen with ytdl( message without tapback ).logger(on error start aria) add thumbsdown
#
# if thumbdown messages not in active screens and message hase no dir/files check for mp4 files!
#   tapback ?
# else
#   tapback thumbs up


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
    d['sqllist'] = sqlite3.connect(d['chatdb']).cursor().execute(f'''SELECT m.text, m.is_from_me, Lm.associated_message_type, m.date FROM message m
                JOIN chat_handle_join ON m.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id
                LEFT JOIN message Lm ON Lm.associated_message_guid like '%' || m.guid                           --connect tapbacks with original message
                LEFT JOIN chat_recoverable_message_join ON chat_recoverable_message_join.message_id = m.ROWID   --connect deleted with messages
                WHERE (chat.chat_identifier="{secs.mail}" OR chat.chat_identifier="{secs.phone}")               --filter messages form cretain sender
                AND m.associated_message_guid IS NULL                                                           --exclude tapback messages
                AND chat_recoverable_message_join.message_id IS NULL                                            --exclude deleted messages
                AND (m.text like 'http%' OR m.text like 'to%')                                                 --filter relevant texts
                AND m.text IS NOT NULL                                                                          --some texts are null perhaps edits
                ORDER BY m.text DESC;                                                                           --sorts vpn befor http texts''').fetchall()  # sql connect make cursor execute query wait for query to finish

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

    # parse() -> for cleanup         -> !!tapbacks        [date, text, prio, screen name, finalfile, tapback] make sure already deleted messages are not in this list anymore
    #            for todo message    -> notapbacks        [date, text, prio, screen name, finalfile, tapback] make sure this hase no message wich are already associated with a tapback
    #            for tocheck message -> thumbdowntapbacks [date, text, prio, screen name, finalfile, tapback]
    # or comebine all in one list containing tapback status messages[(date, text, screen name, finalfile, tapback), (...), ...] # sort so that vpn message is on top

tupl[0].replace('http://', '').split('/',1)
# add screen commands to sql lists in the beninging here
    for item in d['sqllist']:
        item.append(f'{item[0].split('/',3)[2].replace('.',' ')}{item['date']}') # appending dir to put files in
        item.append(f'{item['date']}') # screen name
        if item[] item.append(f'') # appending command

# perhaps use for item in d['todos'] list loop with exit funktion to circumvent list index out of range !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# or try: ... except IndexError: pass     to circumvent list index out of range !!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # SAFETY any active screens and vpn is off -> kill screens
    for panics in any[]:
        kill_screen(panics[date])
        send_message("screen on vpn off")
        sys.exit()

    # message starts 'to' and has !! (from me) and vpn currently on -> vpn off
    for vpncleanup in [message for message in d['sqllist'] if 2004 in message and message[0].startswith('to') and currentloc() != 'de']:
        kill_all_screens()
        screen_vpn_off()
        tapback(message, '!!'); delete(message); break

    # message starts 'http' and has !! (from me) -> specific screen off
    for dlcleanups in [message for message in d['sqllist'] if 2004 in message and message[0].startswith('http')]:
        drop_dl_screen()
        vllt_delete_dl_files()
        tapback(message, '!!'); delete(message); break

    for cleanups in [message for message in d['sqllist'] if 2004 in message]:
        if cleanups[0].startswith('http'): drop_dl_screen(); vllt_delete_dl_files() # message starts 'http' and has !! (from me) -> specific screen off
        if cleanups[0].startswith('to'): kill_all_screens(); screen_vpn_off() # message starts 'to' and has !! (from me) and vpn currently on -> vpn off
        tapback(message, '!!'); delete(message); break


    # message starts 'to' and has None tapback and vpn currently off -> vpn on
    for vpntodo in [message for message in d['sqllist'] if None in message and message[0].startswith('to') and currentloc() == 'de']
        screen_vpn_on()
        tapback(message, 'dislike'); break

    # message starts 'http' and has None tapback and vpn currently on -> dl on
    for dltodo in [message for message in d['sqllist'] if None in message and message[0].startswith('http') and currentloc() != 'de']
        screen_dl_on()
        tapback(message, 'dislike'); break

    for todos in [message for message in d['sqllist'] if None in message]: # vpn should be on top cause of sql sort
        if todos[0].startswith('to') and d['currentloc'] != 'de': screen_dl_on() # message starts 'http' and has None tapback and vpn currently on -> dl on
        if todos[0].startswith('http') and d['currentloc'] == 'de': screen_vpn_on() # message starts 'to' and has None tapback and vpn currently off -> vpn on
        tapback(message, 'dislike'); break


    # message starts 'to' and has dislike and has no active screen and vpn currently on -> tapback like
    for vpnwaiting in [message for message in d['sqllist'] if 2002 in message and message[0].startswith('to') and message[date] not in active_screens and currentloc() != 'de']
        tapback(message, 'like'); break

    # message starts 'http' and has dislike and has no active screen and has mp4/mp3-> tapback like
    for dlwaiting in [message for message in d['sqllist'] if 2002 in message and message[0].startswith('http') and message[date] not in active_screens and mp4/mp3 in os.listdir(message[dir])]
        tapback(message, 'like'); break

    # message starts 'http' and has dislike and has no active screen and has n mp4/mp3 -> tapback?
    for dlwaiting in [message for message in d['sqllist'] if 2002 in message and message[0].startswith('http') and message[date] not in active_screens and mp4/mp3 not in os.listdir(message[dir])]
        tapback(message, '?'); break



    # prio 1 cleanup messages -> massage with !! -> tapback !! -> delete -> exit
    # for message in !!tapbacks[]: tapback(messagetext, !!) -> drop screen name / screen vpn off -> delete(messagetext)
    # for is better for exeting after one entry
    for cleanups in [message for message in d['sqllist'] if 2004 in message and 0 in message]: # list comprehension filters !! messages (2004) from me (0)
        tapback(cleanups[1][1], '!!') # take first item from list of all messages with !! and tapback !!
        if cleanups[1].startswith('to') and d['currentloc'] != 'de': vpnoff() and dropalldlscreens # if text is vpn text shut down vpn and drop all screens
        if cleanups[1].startswith('http') and cleanups[date] in active_screens: dropscreen(cleanups[date])  # if not vpn text just drop specific screeen
        deletemessage(cleanup[1][1]) # delete message with text
        return len(messages); sys.exit() # sys exit after cleanup


    # prio 2 act on message -> message no tapback -> tapback thumbdown -> screen dlp( message ) with logger on error starts aria( message ) / screen set vpn / ignore -> exit
    #    make sure vpn gets handled first
    # for message in notapbacks[]: tapback(messagetext, thumbdown) -> start screen dl(message) / screen vpn on / ignore
    for todos in [message for message in d['messages'] if None in message]:
        tapback(acton[1], 'thumbsdown') # take first item from list of all messages with no tapbacks and tapback thumbsdown
        if acton[1] == 'to ...': screen vpn on; break
        else if vpn ok: dl(acton[1]); break

    for vpntodo in [message for message in d['sqllist'] if None in message and message[0].startswith('to') and currentloc() != 'de']:
        scree_startvpn()


    # alway message with thumb down   -> check active screen and final file is correct (this includes set vpn) -> tapback thumbsup or ? -> exit
    #    make sure vpn gets handled first
    # for message in thumbsdown[]: check screen name not up and finalfile present -> tapback thumbs up
    for waiting in [message for message in d['messages'] if 2002 in message and 1 in message and message[0] not in active_screens]: #  list comp filters disliked messages (2002) from mini (1)
        if waiting[1][3] in os.listdir: # if any mp4 in os list dir thats a thumbs up
            tapback(waiting[1][0]), 'like'); break
        else:
            tapback(waiting[1][0], '?'); break


thumbsdownlist = [message for message in d['messages'] if 'thumbsdown' in message]
not_active_anymore = [message for message in thumbsdownlist if message[2] not in active screens]
in_oslistdir = [message for message in thumbsdownlist if message[3] in oslistdir]


thumbsuplist = [message for message in not_active_anymore if message[3] in oslistdir]
qlist = [message for message in not_active_anymore if message[3] not in oslistdir]

if any(message[3] in os.listdir for message in not_active_anymore): tapback('thumbsup') else tapback('?')




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
