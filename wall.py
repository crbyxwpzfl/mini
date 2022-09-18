
import sys
sys.path.append('/Users/mini/Downloads/transfer/reposetories/private/')
import privates
from requests.auth import HTTPDigestAuth
import json
import requests
import math
import os        
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings

def Get():    # assumes arc turns volume 0 and powerbutton turns volume 0
    response = requests.get(f'https://{privates.ip}:1926/6/audio/volume', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    d['Brightness'] = json.loads(response.content)['current']    # adds 'Brightness'
    print(d.get(sys.argv[3].strip("''"), int(d['Brightness']/d['Brightness']) if d['Brightness'] else 0 ))    # prints 'Brightness' or calculates 'On'

def Set():    # assumes 'Brightness' and 'On' get sent together otherwise this will lag until on
    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    if json.loads(response.content)['powerstate'] == 'On' and sys.argv[3].strip("''") == 'Brightness':    # change volume when On
        requests.post(f'https://{privates.ip}:1926/6/audio/volume', timeout=2, json={'muted': 'false', 'current': int(sys.argv[4].strip("''")) }, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    if json.loads(response.content)['powerstate'] == 'Standby' or (sys.argv[4].strip("''") == 0 and sys.argv[3].strip("''") == 'Brightness'):    # press powerbutton just once! when vlaue 0 or when in Standby
        requests.post(f'https://{privates.ip}:1926/6/input/key', timeout=2, json={'key': 'Standby'}, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))

d = {'Set': Set, 'Get': Get}
d.get(sys.argv[1].strip("''"))()