#!/usr/bin/env zsh

#chmod a+x /current/file
# get info default open with terminal so kind is shell script then add this to login items

# for some reason just a onliner starts both screens
sleep 5; screen -S vs -d -m code-server serve; sleep 5; screen -S hb -d -m homebridge;

# pulling gh changes
#python3 /Users/mini/Downloads/transfer/reps/privates/git.py -pull

# open as for a few minutes
#/Users/mini/Library/Android/sdk/emulator/emulator -avd as
