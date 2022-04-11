#import privates variable
import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates

#ip = privates.ip
#user = privates.user
#pw = privates.pw
#minipath = privates.minipath

import os
from requests.auth import HTTPDigestAuth
import requests
import time
import subprocess
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings





def onoffstate():
    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(privates.user, privates.pw))
    if "On" in str(response.content):
        return 1

def hdmi(data):
    with open(os.path.join(privates.minipath, 'source.txt'), "r+") as f: # open file as read and wirte
        if data != "read":  # if data read do not wirte
            f.write(data)   # write data
            f.truncate()    # delete rest of file
        f.seek(0)           # go to beniging of file               
        try:
            return f.read() # return read hold back by try 
        finally:
            f.close()       # finally closes file then releases return  

def post(path, data):
    response = requests.post(f'https://{privates.ip}:1926/6/{path}', timeout=2, json=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))




if sys.argv[3].strip("''") == "name": # rturns name and stops script
    print("mini")
    sys.exit()


if '"AppleClamshellState" = Yes' in  str(subprocess.Popen(['ioreg', '-r', '-k', 'AppleClamshellState'], stdout=subprocess.PIPE).stdout.read()): # if lid closed
    if int(hdmi("read")) == 2 : # if hdmi2 switch to hdmi1 and turn tv off and write hdmi1 in sourcetxt
        post("activities/launch", {'intent': {'extras': {'query': 'hdmi 1'}, 'action': 'Intent {  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }', 'component': {'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'}}})
        time.sleep(4)
        post("input/key", {'key': 'Standby'})
        hdmi("1")
    print("OCCUPANCY_NOT_DETECTED")
    sys.exit()
        
if '"AppleClamshellState" = No' in  str(subprocess.Popen(['ioreg', '-r', '-k', 'AppleClamshellState'], stdout=subprocess.PIPE).stdout.read()): # if lid open 
    if onoffstate() == None: # if tv off turn tv on
        post("input/key", {'key': 'Standby'})
        time.sleep(4)
    if int(hdmi("read")) == 1: # if sourcetxt hdmi1 switch to hdmi2 
        post("activities/launch", {'intent': {'extras': {'query': 'hdmi 2'}, 'action': 'Intent {  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }', 'component': {'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'}}})
        hdmi("2")
    print("OCCUPANCY_DETECTED")
    sys.exit()