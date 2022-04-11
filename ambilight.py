



# imports and  variables

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
from requests.auth import HTTPDigestAuth
import requests
import math
import os        
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings




# support fuctions

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

def post(body):
    try:
        response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, data=body)
    except requests.exceptions.ConnectionError:
        print("  ----  error connecting setting ambi ----  ")
        sys.exit()
    except requests.exceptions.Timeout:
        print("  ----  timeout error setting ambi  ----  ")
        sys.exit()

def convert():
    h = float(((int(rw("read", "Hue.txt"))-7)%360)/360) #((x-farb angleichung)%360 rest ist neuer hue wert)/360 ausgabe von 0-1
    s = float(math.pow((int(rw("read", "Saturation.txt"))/100),0.5)) #(x/100)^0.5 um tv saturation settings aus zu gleichen
    v = float(rw("read", "Brightness.txt"))/100
    

    if s == 0.0: v*=255; r, g, b = v, v, v
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: r, g, b = v, t, p
    if i == 1: r, g, b = q, v, p
    if i == 2: r, g, b = p, v, t
    if i == 3: r, g, b = p, q, v
    if i == 4: r, g, b = t, p, v
    if i == 5: r, g, b = v, p, q

    return f"{{r: {int(r)}, g: {int(g)}, b: {int(b)}}}"




# logic and output

if sys.argv[1] == "Get":
    print(rw("read", str(sys.argv[3].strip("''"))+'.txt'), end='')
    sys.exit()


if sys.argv[1] == "Set":   
    if  onoffstate() == None: # if tv is off
        if sys.argv[3].strip("''") == "On" and int(sys.argv[4].strip("''")) == 0: # if characteristic On and value off
            post("{r: 0, g: 0, b: 0}")
            rw(sys.argv[4].strip("''"), str(sys.argv[3].strip("''"))+'.txt')
            sys.exit()
        
        rw(sys.argv[4].strip("''"), str(sys.argv[3].strip("''"))+'.txt')         # any other case set characteristic value
        post(convert())
        sys.exit()
