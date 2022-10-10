#!/usr/bin/env python3

# chmod +x /current/file && cd "/current/" && git config core.filemode true && git commit -am "commit chmodx" && git -c core.sshCommand="ssh -i /path/to/priv" push

import os
import pathlib
import subprocess
import time

def sub(cmdstring, waitforcompletion): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if waitforcompletion: print(p.communicate()[0].decode()) # this will wait for subprocess to finisih 

print( os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'config.json')) )

sub(f"screen -S hb -d -m homebridge -U {os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config.json'))} ",False) #  summon hb
time.sleep(2)
sub("screen -S vs -d -m code-server serve",False) #  summon vs
time.sleep(2)
sub("python3 /Users/mini/Downloads/transfer/reps/privates/git.py -pull",True)  # pulling gh changes
print("as up 10 sec close to stop")
time.sleep(10)
sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"/Users/mini/Library/Android/sdk/emulator/emulator -avd as; exit;\"' -e 'set miniaturized of window 1 to false' -e 'end tell'", False) # open as for a few minutes
time.sleep(60*15) #  15 min
sub("/Useres/mini/Library/Android/sdk/platform-tools/adb -e emu kill",True)

sys.exit()
