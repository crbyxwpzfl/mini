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


#lid zu
if '"AppleClamshellState" = Yes' in out:
	print("OCCUPANCY_NOT_DETECTED")
    #for now do nothing in the furure turn tv off

#lid auf
elif '"AppleClamshellState" = No' in out:
    
    #ad detection for source state
    #only switch source if in hdmi1 
    if int(status) == 0:
        data = '{key: "Standby"}'
        response = requests.post(f'https://{privates.ip}:1926/6/input/key', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
        time.sleep(2)

        data = {'intent': {'extras': {'query': 'hdmi 2'}, 'action': 'Intent {  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }', 'component': {'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'}}}
        response = requests.post(f'https://{privates.ip}:1926/6/activities/launch', timeout=2, json=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))

    print("OCCUPANCY_DETECTED")    
    sys.exit()