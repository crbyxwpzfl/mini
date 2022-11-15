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

def parsereadlist():  # when foldername not in downloaddir add url to aria or dlp dict
    d['sqllist'] = sqlite3.connect('/Users/mini/Library/Messages/chat.db').cursor().execute(f'''SELECT m.text, m.date, Lm.associated_message_type, m.is_from_me FROM message m
                JOIN chat_handle_join ON m.handle_id = chat_handle_join.handle_id JOIN chat ON chat.ROWID = chat_handle_join.chat_id
                LEFT JOIN message Lm ON Lm.associated_message_guid like '%' || m.guid                           --connect tapbacks with original message
                LEFT JOIN chat_recoverable_message_join ON chat_recoverable_message_join.message_id = m.ROWID   --connect deleted with messages
                WHERE (chat.chat_identifier="{secs.mail}" OR chat.chat_identifier="{secs.phone}")               --filter messages form cretain sender
                AND m.associated_message_guid IS NULL                                                           --exclude tapback messages
                AND chat_recoverable_message_join.message_id IS NULL                                            --exclude deleted messages
                AND (m.text like 'http%' OR m.text like 'to%')                                                  --filter relevant texts
                AND m.text IS NOT NULL                                                                          --some texts are null perhaps edits
                ORDER BY m.text DESC;                                                                           --sorts vpn befor http texts''').fetchall()  # sql connect make cursor execute query wait for query to finish

def sort():  # NOTE algorythm for auto naming is f hard to do  # sorts all in current working dir
    d['srts'] = d['searchfiles']( d['files'](os.getcwd()) , 'srt')  # this collects all srts of dirs for ffmpeg
    [ list(  map(d['ffmpeg'], enumerate(x))) for x in d['files'](os.getcwd())]  # TODO list(...) hopefully is not nedded later just for debugging # hopefully get rid of Null lists

def dl():  # NOTE consider --allow-overwrite=true/'overwrite': True, # sysargv2 is todos[0]/message text and since both aria and dlp default to dl in current dir and we call screen after change to correct dir cause of logging for screen no need for out dir specification
    try: import yt_dlp; print(yt_dlp.YoutubeDL({'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'ignoreerrors': True, 'restrictfilenames': True}).extract_info(sys.argv[2], download=True)['title']) # cant use this to just extract url since aria does not support hls 'format_id' to verify selection 
    except (yt_dlp.utils.UnsupportedError, yt_dlp.utils.DownloadError, TypeError): 
        sub(f'aria2c "{sys.argv[2].split("/",3)[3]}" --save-session={os.path.join(pathlib.Path(__file__).resolve().parents[0], "ariasfile.txt")} --seed-time=0', True)  # use safefile with --input-file /path/to/ariasfile.txt to resume any stoped downloads
        sort()

def tapback(message, tapordel):  # this is inline just for simplyfinging edits for futur ui changes (like/2/2001 dislike/3/2002 !!/5/2004 ?/6/2005)
    sub(f""" osascript -e '
        tell application \"System Events\" to tell process \"Messages\"
            set frontmost to true
            tell application \"System Events\" to keystroke \"f\" using command down
            tell application \"System Events\" to keystroke \"{message}\"
            tell application \"System Events\" to keystroke return
            delay 1
            perform action \"AXPress\" of static text 2 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1
            delay 1
            set smalerlist to (entire contents of group 1 of group 1 of group 1 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1 as list)
            repeat with n from 1 to count of smalerlist 
                if (value of item n of smalerlist contains \"{message}\") then --to get this loop right use xcodes accssesebilety inspector and the gist findmessage
                    perform action \"AXPress\" of item n of smalerlist
                    exit repeat
                end if
            end repeat
            delay 1
            tell application \"System Events\" to {"key code 17 using command down" if tapordel else "key code 51"} --17 is t and 51 is delete
            tell application \"System Events\" to {f"keystroke {tapordel}" if tapordel else "keystroke return"}
        end tell' """, True)

def head():  # TODO adjust serach message.text length for tpaback message TODO perhaps to much tapbacks and need to sys.exit early # runs all for loops once so worst case cleanups.tapback(!!) + cleanups.tapback(delete) + todos.tapback(dislike) + waitings.tapback(like)
    parsereadlist(); d['screens'](); d['locaway']()

    for panics in [m for m in d['sqllist'] if [l for l in d['sqllist'] if 2004 in l and any(str(s).startswith('to') for s in l)] or not d['locaway']]  # savety list with all messages when there is a !! 'to' message (from me) so vpn wants off or actually is off
        if panics[3].startswith('http'):  sub(f'screen -X -S {panics[1]} quit', True)  # drop all dl screens
        if not d.get('sentpanic'):        sub(f"osascript -e 'tell application \"Messages\" to send \"dls but vpn off\" to participant \"{d['phonenr']}\"'", True); d['sentpanic'] = True  # sned panic only once

    for cleanups in [m for m in d['sqllist'] if 2004 in m]:
        if cleanups[0].startswith('http'):                 sub(f'screen -X -S {cleanups[1]} quit', Ture); tapback(celanups[0], 5); tapback(cleanups[0], False); break  # http message and has !! (from me) - specific screen off
        if cleanups[0].startswith('to') and d['locaway']:  sub(d['sshspinala'](todos[1], 'disconnect'), True); tapback(celanups[0], 5); tapback(cleanups[0], False); break  # to message and has !! (from me) and vpn currently on - vpn off

    for todos in [m for m in d['sqllist'] if None in m]:  #TODO before if None in m istead of if not m[3] # vpn should be on top cause of sql sort
        if todos[0].startswith('http') and d['locaway'] and d['screens'].count('(Detached)') < 6:  sub(f'mkdir {d['outdir'](todos[0], todos[1])} && cd {d['outdir'](todos[0], todos[1])} && screen -L -S {todos[1]} -d -m dl {todos[0]}', True); tapback(todos[0], 3); break  # message starts 'http' and has None tapback and vpn currently on and screen sockets less than 6 - dl on
        if todos[0].startswith('to') and not d['locaway']:                                         sub(d['sshspinala'](todos[1], f'connect {todos[0][:-2]}'), True); tapback(todos[0], 3); break  # message starts 'to' and has None tapback and vpn currently off - vpn on

    for waitings [m for m in d['sqllist'] if 2002 in m and m[1] not in d['screens']]  # has dislike and has no active screen
        if ( waitings[0].startswith('http') and d['locaway'] ) or ( mp4/mp3 in os.listdir(message[dir]) ):             tapback(waitings[0], 2); break  # message has no active screen and complete condition true -> tapback like

        tapback(waitings[0], 2) if waitings[0].startswith('http') and d['searchfiles'](d['files'](d['outdir'](waitings[0], waitings(1))), 'mp4') else tapback(waitings[0], 6); break  # message 'http....' has no screen and in outdir is mp4 -> tapback like else tapback ?
        tapback(waitings[0], 2) if waitings[0].startswith('to') and d['locaway'] else tapback(waitings[0], 6); break  # message 'to....' has no screen and locaway is True so vpn ok -> tapback like else tapback ?

    print(d.get(sys.argv[3].strip("''"), len([m for m in d['sqllist'] if None in m]) ))  # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge

def helps():
    print("""

        /humidreadlist.py get value ofdict      runs head and prints d['ofdict'] value for debugging

        /humidreadlist.py sort                  sorts current dir with naming convention ..../current dir date/current dir.mp4

        /humidreadlist.py dl http://dir.name    ups dl without any safegurads

        /humidreadlist.py get                   runs head and returns count of todos

    """)


d = {'get': head, 'dl': dl, 'sort': sort, # defs for running directly in cli via arguments
    'sshspinala':   lambda whereto, date: f'screen -S {date} -d -m ssh spinala@192.168.2.1 -i {secs.minisshpriv} nordvpn {whereto}',
    'outdir':       lambda message, date: os.path.join('/Users/mini/Downloads/temps/', f'{message.split("/",3)[2].replace("."," ")} {date}'),  # TODO perhaps change temps to desktop dir # slpit() creates list like ['http:', '', 'final.file.whatever', 'url'] so mkdir to dl to makes ..../temp/final file whatever date/  # so naming convention is http://final.file.whatever/url
    'ffmpeg':       lambda f:             print(f"""ffmpeg -n -i \"{f[1]}\" { f'-i "{d['srts'][-1]}"' if d.get('srts') else "-map 0" } -metadata title= -vcodec copy -acodec copy -scodec \"mov_text\" -ac 8 \"{' '.join(f.split('/')[5].split(' ')[:-1])} {f[0] + 1 if f[0] else ''}.mp4\" """)   # f[1] is ..../temps/final file whatever date/ so f.split[5].split[:-1] makes ..../temps/final file whatever date/final file whatever.mp4 plus append nr of file starting with 2
    'locaway':      lambda:               True if requests.get(f'http://ipinfo.io/json', timeout=2, verify=False).json().get('country', "DE").lower() != 'de' else False,  # everything but de will be treated as vpn on this is very bad here no https cause of error message
    'screens':      lambda:               sub('screen -list', True)  # sub returns cmd output as string and then in listcomp for waitings date is unique in string
    'files':        lambda filesdir:      [  sorted([f'{p}/{n}' for n in f if n.endswith("mkv") or n.endswith("avi") or n.endswith("srt")])  for p, s, f in os.walk(filesdir)],  # [ ['dir1/file1.mkv', 'dir1/file2.srt'], ['dir2/file1.mkv', 'dir2/file2.srt']  ] but with a lot of empty lists if subdir has no matches
    'searchfiles':  lambda files, end:    [f for sl in files for f in sl if f.endswith(end) and 'en' in f.lower()]  # [dir1/file2.srt, dir2/file2.srt]
    }

d.get(sys.argv[1].strip("''").lower(), helps)()  # call head() with 'Get' from homebridge or helpes()
