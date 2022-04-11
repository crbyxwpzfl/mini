#import privates variable
import sys
import os
#sys.path.append(os.environ.get('privates'))
sys.path.append('/Users/mini/Downloads/private/')
import privates

import subprocess
import requests
from requests.auth import HTTPDigestAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

#asume tv is off
status = 0

characteristic = sys.argv[3].strip("''")

if characteristic == "name":
    print("test")
    sys.exit()

#check if tv is off if tv is on status = 1
response = requests.get(f'https://{privates.ip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(privates.user, privates.pw))
if "On" in str(response.content):
    status = 1

#detect lid status
output = subprocess.Popen(['ioreg', '-r', '-k', 'AppleClamshellState'], stdout=subprocess.PIPE)
out = str(output.stdout.read())

#read current hdmi state from source.txt
f = open(os.path.join(privates.minipath, 'source.txt'), 'r')
hdmi = f.read()
f.close()

#lid zu
if '"AppleClamshellState" = Yes' in out:

    #if in hdmi2 turn tv off and wirte hdmi 1 to source.txt
    if int(hdmi) == 2:
        data = '{key: "Standby"}'
        response = requests.post(f'https://{privates.ip}:1926/6/input/key', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
        
        f = open(os.path.join(privates.minipath, 'source.txt'), 'w')
        f.write('1')
        f.close()
    
    print("OCCUPANCY_NOT_DETECTED")

#lid auf
if '"AppleClamshellState" = No' in out:
    
    #ad detection for source state
    #only switch source if in hdmi1 
    if int(status) == 0:
        data = '{key: "Standby"}'
        response = requests.post(f'https://{privates.ip}:1926/6/input/key', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))

    if int(hdmi) == 1:
        time.sleep(2)
        data = {'intent': {'extras': {'query': 'hdmi 2'}, 'action': 'Intent {  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }', 'component': {'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'}}}
        response = requests.post(f'https://{privates.ip}:1926/6/activities/launch', timeout=2, json=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))

        f = open(os.path.join(privates.minipath, 'source.txt'), 'w')
        f.write('2')
        f.close()
    
    print("OCCUPANCY_DETECTED")    
    sys.exit()