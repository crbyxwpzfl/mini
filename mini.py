#!/usr/bin/env python3

# chmod +x /current/file && cd "/current/" && git config core.filemode true && git commit -am "commit chmodx" && git -c core.sshCommand="ssh -i /path/to/priv" push

import os
import pathlib
import subprocess
import time

def sub(cmdstring, waitforcompletion): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if waitforcompletion: print(p.communicate()[0].decode()) # this will wait for subprocess to finisih 

time.sleep(4); print(); print(); print("-------- node status")  #print all versions off manually installed packages so no python since python comes with macos
sub("npm view node",True)
sub("node -v",True)

print(); print(); print("-------- npm status")
sub("npm -g ls",True)
sub("npm -g outdated",True)

print(); print(); print("-------- pip status")
sub("python3 -m pip list",True)
sub("python3 -m pip list --outdated",True)

print(); print(); print("-------- aria status")
sub("aria2c --version",True)

print(); print(); print("-------- ffmpeg status")
sub("ffmpeg --version",True)

print(); print(); print("-------- vs status")
sub("code-server --version",True)


print(); print(); print("staggerd up of hb and vs")
time.sleep(4); sub("screen -S vs -d -m code-server serve",False) #  summon vs
time.sleep(4); sub(f"screen -S hb -d -m homebridge -U {os.path.abspath(os.path.dirname( __file__ ))}",False) #  summon hb
time.sleep(2); sub("screen -list",True)

print(); print(); print("pull changes of of gh")
time.sleep(2); sub("python3 /Users/mini/Downloads/transfer/reps/privates/git.py -pull",True)  # pulling gh changes


print(); print(); print("as up 10 sec close to stop")
time.sleep(10); sub(f"osascript -e 'tell app \"Terminal\"' -e 'do script \"/Users/mini/Library/Android/sdk/emulator/emulator -avd as; exit;\"' -e 'set miniaturized of window 1 to false' -e 'end tell'", False) # open as for a few minutes
time.sleep(60*15); sub("/Useres/mini/Library/Android/sdk/platform-tools/adb -e emu kill",True)


sys.exit()
