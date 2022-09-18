

import sys; sys.path.append('/Users/mini/Downloads/transfer/reps/privates/'); import secs  # fetch secrets

from requests.auth import HTTPDigestAuth
import requests
import fileinput
import pathlib # for calling itself for overwrite
import subprocess
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings

def post(path, data):
    response = requests.post(f'https://{secs.wallip}:1926/6/{path}', timeout=2, data=data, verify=False, auth=HTTPDigestAuth(secs.walluser, secs.wallpw))

def Get():
    d['tv'] = 1 if "On" in str(requests.get(f'https://{secs.wallip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(secs.walluser, secs.wallpw)).content) else 0
    d['mini'] = 0 if '"AppleClamshellState" = Yes' in  str(subprocess.run(['ioreg', '-r', '-k', 'AppleClamshellState'], stdout=subprocess.PIPE).stdout.decode()) else 1

    if d['mini'] == int(d['hdmi'] - 1) or (d['tv'] == 0 and d['mini'] == 1): # switch hdmi turns tv on automaticly
        post("activities/launch", f"{{'intent': {{'extras': {{'query': 'hdmi {d['hdmi']}'}}, 'action': 'Intent {{  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }}', 'component': {{'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'}} }} }} ")
        
        d['line36'] = f"     'hdmi': {3 - int(d['hdmi'])},\n" # prints 2 if was 1 and 1 if was 2 to 'hdmi'
        for line in fileinput.input([pathlib.Path(__file__).resolve()], inplace=True): # open file and overwrite lines
            print(d['line36'], end='') if fileinput.filelineno() == 36 else print(line, end='')

    print(d.get(sys.argv[3].strip("''") , d['mini']  )) # OccupancyDetected is 0 lid closed and 1 lid open

d = {'Get': Get, # defs for running directly in cli via arguments
     'name': 'mini', # characteristics
     'hdmi': 2,
    }
d.get(sys.argv[1].strip("''"), sys.exit)()

# not in use turn tv on and off via state of laptiop lid closed and open