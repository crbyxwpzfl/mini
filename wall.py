



# imports and variables

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
from requests.auth import HTTPDigestAuth
import requests
import math
import subprocess
import os        
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings




# support functions

def post(path, data):
    response = requests.post(f'https://{privates.ip}:1926/6/{path}', timeout=2, json=data, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))

def onoffstate():
    try:
        response = requests.get(f'https://{privates.ip}:1926/6/powerstate', verify=False, timeout=2, auth=HTTPDigestAuth(privates.user, privates.pw))
    except requests.exceptions.ConnectionError:
        print("  ----  error connecting getting powerstate  ----  ")
        sys.exit()
    except requests.exceptions.Timeout:
        print("  ----  timeout error getting powerstate  ----  ")
        sys.exit()
    else:
        if "On" in str(response.content):
            return 1
        else:
            return 0

def rw(data, txt):
    with open(os.path.join(privates.minipath, txt), "r+") as f: # open file as read and wirte
        if data != "read":  # if data read do not wirte
            f.write(data)   # write data
            f.truncate()    # delete rest of file
        f.seek(0)           # go to beniging of file               
        try:
            return f.read() # return read hold back by try 
        finally:
            f.close()       # finally closes file then releases return  




# logic and output

if sys.argv[1] == "Get":
    if sys.argv[3].strip("''") == "Brightness":
        print(rw("read", 'Volume.txt'), end='')
        sys.exit()

    if sys.argv[3].strip("''") == "On":
        print(onoffstate())
        sys.exit()

if sys.argv[1] == "Set":
    if sys.argv[3].strip("''") == "Brightness" and int(onoffstate()) == 1: # if tv off set volume
        post("audio/volume", "{'muted': 'false', 'current': '" + sys.argv[4].strip("''") + "'}")
        rw(sys.argv[4].strip("''"), 'Volume.txt')
        sys.exit()
    
    if sys.argv[3].strip("''") == "On" and int(onoffstate()) == 0 and int(sys.argv[4].strip("''")) == 1: # if characteristic On and tv off and value 1 turn tv on
        post("input/key", "{'key': 'Standby'}")
        sys.exit()
    
    if sys.argv[3].strip("''") == "On" and int(onoffstate()) == 1 and int(sys.argv[4].strip("''")) == 0: # if characteristic On and tv on and value 0 turn tv off
        post("input/key", "{'key': 'Standby'}")
        sys.exit()

