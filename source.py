



# variables and imports

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
from requests.auth import HTTPDigestAuth
import requests
import fileinput
import pathlib # for calling itself for overwrite
import subprocess
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings


def post(path, data):
    response = requests.post(f'https://{privates.ip}:1926/6/{path}', timeout=2, json=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))

def Get():
    d['tv'] = 1 if "On" in str(requests.get(f'https://{privates.ip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(privates.user, privates.pw)).content) else 0
    d['mini'] = 0 if '"AppleClamshellState" = Yes' in  str(subprocess.run(['ioreg', '-r', '-k', 'AppleClamshellState'], stdout=subprocess.PIPE).stdout.decode()) else 1

    if d['mini'] != d['tv']: # switch hdmi turns tv on automaticly
        post("activities/launch", f"{{'intent': {{'extras': {{'query': 'hdmi {d['hdmi']}'}}, 'action': 'Intent {{  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }}', 'component': {{'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'}} }} }} ")
        
        d['line37'] = f"     'hdmi': {3 - int(d['hdmi'])},\n" # prints 2 if was 1 and 1 if was 2 to 'hdmi'
        for line in fileinput.input([pathlib.Path(__file__).resolve()], inplace=True): # open file and overwrite lines
            print(d['line37'], end='') if fileinput.filelineno() == 37 else print(line, end='')

    print(d.get(sys.argv[3].strip("''") , d['mini']  )) # OccupancyDetected is 0 lid closed and 1 lid open

d = {'Get': Get, # defs for running directly in cli via arguments
     'name': 'mini', # characteristics
     'hdmi': 1,
    }
d.get(sys.argv[1].strip("''"), sys.exit)()