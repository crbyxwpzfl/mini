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
    d['ffmpeg'] = lambda f: print(f"""ffmpeg -n -i \"{f[1]}\" { f'-i "{d["srts"][-1]}"' if d.get('srts') and 'en' in d.get('srts').lower() else "-map 0" } -metadata title= -vcodec copy -acodec copy -scodec \"mov_text\" -ac 8 \"{'/'.join(f[1].split('/')[:-1])}/{' '.join(os.getcwd().split('/')[-1].split(' ')[:-1])} {f[0] + 1 if f[0] else ''}.mp4\" """)  #TODO change print here to sub( , False) verbose  # {'/'.join(f[1].split('/')[:-1])}/{' '.join(currdir.split('/')[-2].split(' ')[:-1])}.mp4 makes '..../final file wtv date/posiblysubdir/file.notmp4' to '..../final file wtv date/posiblysubdir/final file wtv.mp4' plus append nr of file starting with 2
    d['srts'] = [d['searchfiles']( d['files'](os.getcwd(), 'srt', 'srt') , 'srt')]  # this collects all srts of dir for ffmpeg
    [ list(map(d['ffmpeg'], enumerate(x))) for x in d['files'](os.getcwd(), 'mkv', 'avi')]  # hopefully get rid of Null lists


def dl():  # NOTE consider --allow-overwrite=true/'overwrite': True, # sysargv2 is todos[0]/message text and since both aria and dlp default to dl in current dir and we call screen after change to correct dir cause of logging for screen no need for out dir specification
    try: import yt_dlp; print(yt_dlp.YoutubeDL({'format_sort': ['ext'], 'keepvideo': True, 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'm4a'}], 'ignoreerrors': True, 'restrictfilenames': True}).extract_info(sys.argv[2], download=True)['title']) # cant use this to just extract url since aria does not support hls 'format_id' to verify selection 
    except (yt_dlp.utils.UnsupportedError, yt_dlp.utils.DownloadError, TypeError): 
        sub(f'aria2c "{sys.argv[2].split("/",3)[3]}" --save-session={os.path.join(os.getcwd(), "ariasfile.txt")} --seed-time=0', True)  # use safefile with --input-file /path/to/ariasfile.txt to resume any stoped downloads
        sort()

# TODO get titel of video for naming dl dir and make this as reliable and as fast as possible # NOTE perhaps use timestamp instead of formatted message to find correct message
def tapback(message, tapordel):  # this is inline just for simplyfinging edits for futur ui changes (like/2/2001 dislike/3/2002 !!/5/2004 ?/6/2005)
    sub(f""" osascript -e '
        tell application \"System Events\" to tell process \"Messages\"
            set frontmost to true
            tell application \"System Events\" to keystroke \"f\" using command down
            tell application \"System Events\" to keystroke \"{message}\"
            tell application \"System Events\" to keystroke return
            delay 2 --to find the correct group hirachy just repeat with n from 1 to count of (entire contents of window 1 as list) log(get description/value/role of item n of (enire.. as list)) end repeat
            if static text 1 of button 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1 exists then
                perform action "AXPress" of static text 1 of button 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1
            else --either press link preview or text result to scroll searchresult to visible area
                perform action "AXPress" of static text 2 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 2 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1
            end if
            delay 1
            repeat with n from 1 to 40 --here 40 is abetrary just has to be high enugh so all messages in visible area get traversed usually les than 20
                if (description of group n of group 1 of group 1 of group 1 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1 contains \"{message.lstrip('http').lstrip('s').strip('://').strip('www.').split('/')[0]}\") then --again searches for sub text of message in description of message group
                    log(get description of group n of group 1 of group 1 of group 1 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1) --logs description to get video title for naming dir to stdout
                    perform action \"AXShowMenu\" of group n of group 1 of group 1 of group 1 of group 1 of group 3 of group 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1 --shows menue to select a message
                    exit repeat
                end if
            end repeat
            delay 1
            tell application \"System Events\" to {"key code 17 using command down" if tapordel else "key code 51"} --17 is t and 51 is delete
            tell application \"System Events\" to {f"keystroke {tapordel}" if tapordel else "keystroke return"}
        end tell' """, True)

def head():  # TODO adjust serach message.text length for tpaback message TODO perhaps to much tapbacks and need to sys.exit early # runs all for loops once so worst case cleanups.tapback(!!) + cleanups.tapback(delete) + todos.tapback(dislike) + waitings.tapback(like)
    parsereadlist(); d['screens'](); d['locaway']()

    for panics in [m for m in d['sqllist'] if [l for l in d['sqllist'] if 2004 in l and any(str(s).startswith('to') for s in l)] or not d['pingout']]:  # savety list with all messages when there is a !! 'to' message (from me) so vpn wants off or actually is off
        if panics[3].startswith('http'):  sub(f'screen -X -S {panics[1]} quit', True)  # drop all dl screens
        if not d.get('sentpanic'):        sub(f"osascript -e 'tell application \"Messages\" to send \"dls but vpn off\" to participant \"{d['phonenr']}\"'", True); d['sentpanic'] = True  # sned panic only once

    for cleanups in [m for m in d['sqllist'] if 2004 in m]:
        if cleanups[0].startswith('http'):                 sub(f'screen -X -S {cleanups[1]} quit', True); tapback(celanups[0], 5); tapback(cleanups[0], False); break  # http message and has !! (from me) - specific screen off
        if cleanups[0].startswith('to') and d['pingout']:  sub(d['sshspinala'](todos[1], 'disconnect'), True); tapback(celanups[0], 5); tapback(cleanups[0], False); break  # to message and has !! (from me) and vpn currently on - vpn off

    for todos in [m for m in d['sqllist'] if None in m]:  #TODO before if None in m istead of if not m[3] # vpn should be on top cause of sql sort
        if todos[0].startswith('http') and d['pingout'] and d['screens']().count('(Detached)') < 6:  sub(f'mkdir {d["outdir"](todos[0], todos[1])} && cd {d["outdir"](todos[0], todos[1])} && screen -L -S {todos[1]} -d -m dl {todos[0]}', True); tapback(todos[0], 3); break  # message starts 'http' and has None tapback and vpn currently on and screen sockets less than 6 - dl on
        if todos[0].startswith('to') and not d['pingout']:                                         sub(d['sshspinala'](todos[1], f'connect {todos[0][:-2]}'), True); tapback(todos[0], 3); break  # message starts 'to' and has None tapback and vpn currently off - vpn on

    for waitings in [m for m in d['sqllist'] if 2002 in m and m[1] not in d['screens']]:  # has dislike and has no active screen
        tapback(waitings[0], 2) if waitings[0].startswith('http') and d['searchfiles'](d['files'](  d['outdir'](waitings[0], waitings(1)), 'mp4', 'mp4'  ), 'mp4') else tapback(waitings[0], 6); break  # message 'http....' has no screen and in outdir is mp4 -> tapback like else tapback ?
        tapback(waitings[0], 2) if waitings[0].startswith('to') and d['pingout'] else tapback(waitings[0], 6); break  # message 'to....' has no screen and locaway is True so vpn ok -> tapback like else tapback ?

    print(d.get(sys.argv[3].strip("''"), len([m for m in d['sqllist'] if None in m]) ))  # print sth from dict for debugging or print count of urls as 'CurrentRelativeHumidity' to homebridge

def helps():
    print(f"""

        /humidreadlist.py get value 'ofdict'    runs head and prints d['ofdict'] value for debugging

        /humidreadlist.py dl http://dir.name    ups dl without any safegurads

        /humidreadlist.py get                   runs head and returns count of todos

        /humidreadlist.py sort                  sorts '{os.getcwd()}/subd/file.notmp4s' to '{os.getcwd()}/subd/{' '.join(os.getcwd().split('/')[-1].split(' ')[:-1])}.mp4s'

    """)  # NOTE perhaps actually list sort files and final files here


d = {'get': head, 'dl': dl, 'sort': sort, # defs for running directly in cli via arguments
    'sshspinala':   lambda whereto, date:       f'screen -S {date} -d -m ssh spinala@192.168.2.1 -i {secs.minisshpriv} nordvpn {whereto}',
    'outdir':       lambda message, date:       os.path.join('/Users/mini/Downloads/temps/', f'{message.split("/",3)[2].replace("."," ")} {date}'),  # TODO perhaps change temps to desktop dir # slpit() creates list like ['http:', '', 'final.file.whatever', 'url'] so mkdir to dl to makes ..../temp/final file whatever date/  # so naming convention is http://final.file.whatever/url
    'locaway':      lambda:                     d['pingout'] = True if requests.get(f'http://ipinfo.io/json', timeout=2, verify=False).json().get('country', "DE").lower() != 'de' else False,  # everything but de will be treated as vpn on this is very bad here no https cause of error message
    'screens':      lambda:                     sub('screen -list', True),  # sub returns cmd output as string and then in listcomp for waitings date is unique in string
    'files':        lambda filesdir, one, two:  [  sorted([f'{p}/{n}' for n in f if n.endswith(one) or n.endswith(two)])  for p, s, f in os.walk(filesdir)],  # [ ['dir1/file1.mkv', 'dir1/file2.srt'], ['dir2/file1.mkv', 'dir2/file2.srt']  ] but with a lot of empty lists if subdir has no matches
    'searchfiles':  lambda files, end:          [f for sl in files for f in sl if f.endswith(end)]  # [dir1/file2.srt, dir2/file2.srt]
    }


d.get(sys.argv[1].strip("''").lower(), helps)()  # call head() with 'Get' from homebridge or helpes()
