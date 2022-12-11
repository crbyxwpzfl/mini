#!/usr/bin/env python3
# chmod +x /current/file && cd "/current/" && git config core.filemode true && git commit -am "commit chmodx" && git -c core.sshCommand="ssh -i /path/to/priv" push


#let cluster fuck begin




import sys; sys.path.append('/Users/mini/Downloads/transfer/reps-privates/'); import secs  # fetch secrets

import os
import subprocess
import pathlib  # for calling itself in dl()
import yt_dlp  # for dlp()
import requests  # for currentloc()
import sqlite3  # for parsereadlist()


def sub(cmdstring, silence):  # string here because shell true because only way of chaning commands esp important for tapback()
    if silence: return subprocess.Popen(cmdstring , shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode()  # default universalnewlines/text False is ok because of decode()
    if not silence: subprocess.Popen(cmdstring , shell=True, stdout=sys.stdout, stderr=sys.stderr).wait()  # unlike aboveus this prints output to current stdout not quiet and waits for completion

def parsereadlist():  # NOTE later in head() all messages with a revocked tapback have 300X in Lm.assciated not None perhaps causes issues with listcomperhensions in herad()
    d['sqllist'] = sqlite3.connect('/Users/mini/Library/Messages/chat.db').cursor().execute(f'''SELECT m.text, m.date, Lm.associated_message_type, m.is_from_me FROM message m
                JOIN chat_handle_join ON m.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id
                LEFT JOIN message Lm ON Lm.associated_message_guid like '%' || m.guid                           --connect tapbacks with original message
                LEFT JOIN chat_recoverable_message_join ON chat_recoverable_message_join.message_id = m.ROWID   --connect deleted with messages
                WHERE (chat.chat_identifier="{secs.mail}" OR chat.chat_identifier="{secs.phone}")               --filter messages form cretain sender
                AND m.associated_message_guid IS NULL                                                           --exclude tapback messages
                AND chat_recoverable_message_join.message_id IS NULL                                            --exclude deleted messages
                AND (m.text like 'http%' OR m.text like 'to%')                                                  --filter relevant texts
                AND m.text IS NOT NULL                                                                          --some texts are null perhaps edits
                ORDER BY m.text DESC;                                                                           --sorts vpn befor http texts''').fetchall()  # NOTE order desc is important so to message is handled first  # sql connect make cursor execute query wait for query to finish

def sort():  # NOTE algorythm for auto naming is f hard to do  # sorts all in current working dir
    d['ffmpeg'] = lambda f: print(f"""ffmpeg -n -i \"{f[1]}\" { f'-i "{d["srts"][-1]}"' if d.get('srts') and 'en' in d.get('srts').lower() else "-map 0" } -metadata title= -vcodec copy -acodec copy -scodec \"mov_text\" -ac 8 \"{'/'.join(f[1].split('/')[:-1])}/{' '.join(os.getcwd().split('/')[-1].split(' ')[:-1])} {f[0] + 1 if f[0] else ''}.mp4\" """, False)  #TODO change print here to sub( , False) verbose  # {'/'.join(f[1].split('/')[:-1])}/{' '.join(currdir.split('/')[-2].split(' ')[:-1])}.mp4 makes '..../final file wtv date/posiblysubdir/file.notmp4' to '..../final file wtv date/posiblysubdir/final file wtv.mp4' plus append nr of file starting with 2
    d['srts'] = [d['searchfiles']( d['files'](os.getcwd(), 'srt', 'srt') , 'srt')]  # this collects all srts of dir for ffmpeg
    [ list(map(d['ffmpeg'], enumerate(x))) for x in d['files'](os.getcwd(), 'mkv', 'avi')]  # hopefully gets rid of Null lists

def dl():  # NOTE consider --allow-overwrite=true/'overwrite': True, # sysargv2 is todos[0]/message text and since both aria and dlp default to dl in current dir and we call screen after change to correct dir cause of logging for screen no need for out dir specification
    try: import yt_dlp; print(yt_dlp.YoutubeDL({'verbose': True, 'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'ignoreerrors': True, 'restrictfilenames': True}).extract_info(sys.argv[2], download=True)['title'])  # cant use this to just extract url since aria does not support hls use 'format_id' to verify selection
    except (yt_dlp.utils.UnsupportedError, yt_dlp.utils.DownloadError, TypeError): 
        sub(f'aria2c "{sys.argv[2].split("/",3)[3]}" --save-session={os.path.join(os.getcwd(), "ariasfile.txt")} --seed-time=0', True)  # use safefile with --input-file /path/to/ariasfile.txt to resume any stoped downloads
        print(f'aria2c "{sys.argv[2].split("/",3)[3]}" --save-session={os.path.join(os.getcwd(), "ariasfile.txt")} --seed-time=0', True)  # use safefile with --input-file /path/to/ariasfile.txt to resume any stoped downloads
        print("envocing sort"); sort()

        # TODO perhaps lookinto how to catch extractor error

def tapback(message, emote):  # this is inline just for simplyfinging edits for futur ui changes (like/2/2001 dislike/3/2002 !!/5/2004 ?/6/2005)  # NOTE searches for first 100 chars of message
    d['title'] = sub(f""" osascript -e '
        tell application "System Events" to tell process "Messages"
            set value of text field 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1 to \"{message[:100]}\"
            
            delay 1.0    --to find the correct group hirachy just repeat with n from 1 to count of (entire contents of window 1 as list) log(get description/value/role of item n of (enire.. as list)) end repeat or use automator watch me do and copy steps to script editor
            perform action "AXPress" of static text {"1 of button 1" if message.startswith('https://') else "2 of group 1 of group 3"} of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1
            
            delay 1.0    --find second or first group whose contains either message text or title of preview
            set previewormessage to {"description of static text 1 of button 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1" if message.startswith('https://') else '"'+message.replace('http://','').replace('https://','').split('/')[0]+'"' }
            perform action "AXShowMenu" of {"" if message.startswith("http") else "group 1 of"} (UI element 1 of group 1 of group 1 of group 1 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1 whose description contains previewormessage)

            perform action "AXPress" of menu item "{"Tapback…" if emote else "Delete…"}" of menu 1 of group 1 of window 1
            delay 1.0    --this is slower than keystroke command t + 1 but works wihle messages is in background
            perform action "AXPress" of button {emote if emote else '"'+"Delete"+'"'} {"of group 1 of group 3 of group 1 of group 2 of group 1 of group 1" if emote else "of sheet 1"} of window 1
        
            delay 1.0    --this delay here so next tapback does not carsh into animation of previous tapback
            log(previewormessage)    --print this for use as folder name
        end tell' """, True).strip('\n')  # since log output trails a \n and newline is converted to ? when mkdir
    if "execution error" in d['title']: sub("""osascript -e 'quit app "Messages"' -e 'delay 2' -e 'tell application "Messages" to activate'""", True); print(d['title']); sys.exit()  # tapback error makes messages restart and exits so nothing happes

def head():  # TODO perhaps to much tapbacks and need to sys.exit early # runs all for loops once so worst case cleanups.tapback(!!) + cleanups.tapback(delete) + todos.tapback(dislike) + waitings.tapback(like)
    parsereadlist(); d['screens'] = d['collscreens'](); d['pingout'] = d['locaway']()   # since u cannot assign inside lambda but like to not ping multible times

    for panics in [m for m in d['sqllist'] if [l for l in d['sqllist'] if 2004 in l and any(str(s).startswith('to') for s in l)] or ( not d['pingout'] and str(m[1]) in d['screens'] )]:  # savety list with all messages when there is a !! 'to' message (from me) so vpn wants off or actually is off
        if panics[0].startswith('http'):  sub(f'screen -X -S {panics[1]} quit', True); d['sendpanic'] = True;  # drop all dl screens
    if d.get('sentpanic'): sub(f"osascript -e 'tell application \"Messages\" to send \"dls but vpn off\" to participant \"{secs.phone}\"'", True); sys.exit()  # sned panic after all screens are dropped and exit

    for cleanups in [m for m in d['sqllist'] if 2004 in m]:
        if cleanups[0].startswith('http'): tapback(cleanups[0], 5); tapback(cleanups[0], False);                           sub(f'screen -X -S {cleanups[1]} quit', True);         break  # http message and has !! (from me) - specific screen off
        if cleanups[0].startswith('to'):   tapback(cleanups[0], 5); tapback(cleanups[0], False); None if d['pingout'] else sub(d['sshspinala'](cleanups[1], 'disconnect'), True); break  # to message and has !! (from me) and vpn currently on - vpn off

        #tapback(cleanups[0], 5); tapback(cleanups[0], False)
        #sub(d['sshspinala'](cleanups[1], 'disconnect'), True) if cleanups[0].startswith('to') and d['pingout'] else sub(f'screen -X -S {cleanups[1]} quit', True); break  # when 'to....' and pingout True disconnect else quit screen when no screen is found nothing happens

    # TODO BIG BIG problem !! cant find http://my.file.name/restofurlreallylong

    for todos in [m for m in d['sqllist'] if None in m]:  #TODO before if None in m istead of if not m[3] # vpn should be on top cause of sql sort
        if todos[0].startswith('http') and d['pingout'] and d['screens'].count('(Detached)') < 6: tapback(todos[0], 3); sub(f'mkdir "{d["outdir"](todos[1])}" && cd "{d["outdir"](todos[1])}" && screen -L -S {todos[1]} -d -m "{pathlib.Path(__file__)}" dl "{todos[0]}"', True); break  # message starts 'http' and has None tapback and vpn currently on and screen sockets less than 6 - dl on
        if todos[0].startswith('to')                    and not d['pingout']:                     tapback(todos[0], 3); sub(d['sshspinala'](todos[1], f'connect {todos[0][-2:]}'), True);                                                                                          break  # message starts 'to' and has None tapback and vpn currently off - vpn on
    None
    for waitings in [m for m in d['sqllist'] if 2002 in m and str(m[1]) not in d['screens']]:  # has dislike and has no active screen
        if waitings[0].startswith('http'): tapback(waitings[0], 2) if d['searchfiles'](d['files'](  [f.path for f in os.scandir('/Users/mini/Downloads/temps/') if f.path.endswith(str(waitings[1]))][0], 'mp4', 'mp4'  ), 'mp4') else tapback(waitings[0], 6); break  # message 'http....' has no screen and in /outdir/subdir with end of m.date/ has mp4s -> tapback like else tapback ?
        if waitings[0].startswith('to'):   tapback(waitings[0], 2) if d['pingout']                                                    else sub(d['sshspinala'](todos[1], f'connect {todos[0][-2:]}'), True); None if d['pingout'] else tapback(waitings[0], 6); break  # message 'to....' has no screen and locaway is True so vpn ok -> tapback like else retry connect and tapback ?

    print(d.get(sys.argv[3].strip("''"), len([m for m in d['sqllist'] if None in m]) ))  # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge

def helps():
    print(f"""

        /humidreadlist.py get value 'ofdict'    runs head and prints d['ofdict'] value for debugging

        /humidreadlist.py dl http://dir.name    ups dl without any safegurads

        /humidreadlist.py get                   runs head and returns count of todos

        /humidreadlist.py sort                  sorts '{os.getcwd()}/subd/file.notmp4s' to '{os.getcwd()}/subd/{' '.join(os.getcwd().split('/')[-1].split(' ')[:-1])}.mp4s'

    """)  # NOTE perhaps actually list sort files and predicted final files here


d = {'get': head, 'dl': dl, 'sort': sort, # defs for running directly in cli via arguments
    'sshspinala':   lambda date, whereto:       f'screen -S {date} -d -m ssh spinala@192.168.2.1 -i {secs.minisshpriv} nordvpn {whereto}',
    'outdir':       lambda date:                os.path.join('/Users/mini/Downloads/temps/', f'{d.get("title","")[:50].replace("."," ")} {date}'),  # form http://final.file.whatever/url makes /outdir/final file whatever date/
    'locaway':      lambda:                     True if requests.get(f'http://ipinfo.io/json', timeout=2, verify=False).json().get('country', "DE").lower() != 'de' else False,  # everything but de will be treated as vpn on this is very bad here no https cause of error message
    'collscreens':  lambda:                     sub('screen -list', True),  # sub returns cmd output as string and then in listcomp for waitings date is unique in string
    'files':        lambda filesdir, one, two:  [  sorted([f'{p}/{n}' for n in f if n.endswith(one) or n.endswith(two)])  for p, s, f in os.walk(filesdir)],  # [ ['dir1/file1.mkv', 'dir1/file2.srt'], ['dir2/file1.mkv', 'dir2/file2.srt']  ] but with a lot of empty lists if subdir has no matches
    'searchfiles':  lambda files, end:          [f for sl in files for f in sl if f.endswith(end)]  # [dir1/file2.srt, dir2/file2.srt]
    }


d.get(sys.argv[1].strip("''").lower(), helps)()  # call head() with 'Get' from homebridge or helpes()
