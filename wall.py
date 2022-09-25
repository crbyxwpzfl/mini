

import sys; sys.path.append('/Users/mini/Downloads/transfer/reps/privates/'); import secs  # fetch secrets

from requests.auth import HTTPDigestAuth
import json
import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings

def set():  # routine is switch hdmi when wall on and volume 0 then presspowerbutton when wall off or volume 0 then set volume when wall on and volume not 0
    if d['Brightness'] >= 1 and sys.argv[3] == 'Brightness' and sys.argv[4] == '0':  # switch hdmi to 2 when set volume 0
        requests.post(f'https://{secs.wallip}:1926/6/activities/launch',  timeout=2, json={'intent': {'extras': {'query': 'hdmi 1'}, 'action': 'Intent {  act=android.intent.action.ASSIST cmp=com.google.android.katniss/com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline flg=0x10200000 }', 'component': {'packageName': 'com.google.android.katniss', 'className': 'com.google.android.apps.tvsearch.app.launch.trampoline.SearchActivityTrampoline'} } } , verify=False, auth=HTTPDigestAuth(secs.walluser, secs.wallpw))
        time.sleep(4)

    if d['Brightness'] == 0 or (sys.argv[3] == 'Brightness' and sys.argv[4] == '0'):  # press power button when wall off or when volume 0
        requests.post(f'https://{secs.wallip}:1926/6/input/key', timeout=2, json={'key': 'Standby'}, verify=False, auth=HTTPDigestAuth(secs.walluser, secs.wallpw))

    if d['Brightness'] >= 1 and sys.argv[3] == 'Brightness' and sys.argv[4] != '0':  #  set volume when wall on and dont change volume to 0 when shutting off
        requests.post(f'https://{secs.wallip}:1926/6/audio/volume', timeout=2, json={'muted': 'false', 'current': int(sys.argv[4]) }, verify=False, auth=HTTPDigestAuth(secs.walluser, secs.wallpw))

d = {
    'Brightness': json.loads(requests.get(f'https://{secs.wallip}:1926/6/audio/volume', timeout=2, verify=False, auth=HTTPDigestAuth(secs.walluser, secs.wallpw)).content)['current']
    }
print(d.get(sys.argv[3], max( min(d['Brightness'],1), 0) )) if sys.argv[1] == 'Get' else set()  # calls set or prints 'Brightness' or calculates/prints 'On' calculation assumes arc turns volume 0 and powerbutton turns volume 0
