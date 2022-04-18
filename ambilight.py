



# imports and  variables

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
from requests.auth import HTTPDigestAuth
import json
import colorsys
import requests
import math
import os        
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable http warnings




# support fuctions

def get(path):
    response = requests.get(f'https://{privates.ip}:1926/6/{path}', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    return response.content

def post(body):
    try:
        response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, json=body)
    except requests.exceptions.ConnectionError:
        print("  ----  error connecting setting ambi ----  ")
        sys.exit()
    except requests.exceptions.Timeout:
        print("  ----  timeout error setting ambi  ----  ")
        sys.exit()


def hsvof(r, g, b):
    (h, s, v) = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return(int(h*360), int(s*100), int(v*100))

def rgbof(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(((h-7)%360)/360, math.pow((s/100),0.5), (v+1)/100)
    return(int(r*255), int(g*255), int(b*255)+1)




# logic and output

if sys.argv[1] == "Get":
    if str(sys.argv[3].strip("''")) == "On":
        d = {'On': 0}   #creates dict and assumes off state
        d[json.loads(get('powerstate'))['powerstate']] = 1 #overwrites key On or creates key Standby
    else:
        d = json.loads(get('ambilight/cached'))['layer1']['left']['0'] #creates dict with keys r g b
        (d['Hue'], d['Saturation'], d['Brightness']) = hsvof(d['r'], d['g'], d['b']) #adds keys Hue Saturation Brightness 
    
    print(d[sys.argv[3].strip("''")])   #returns value of wanted characteristic  
    sys.exit()    


if sys.argv[1] == "Set" :

    #ACHTUNG this is shit redoo this!!!

    d = {'On': 1}   #creates dict and assumes on state
    d[json.loads(get('powerstate'))['powerstate']] = 0 #overwrites key On or creates key Standby
    

    if d['On'] == 1: # only if tv is off
        d.update(json.loads(get('ambilight/cached'))['layer1']['left']['0']) #adds keys r g b
        (d['Hue'], d['Saturation'], d['Brightness']) = hsvof(d['r'], d['g'], d['b']) #adds keys Hue Saturation Brightness 
        d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    #update value of wanted characteristic
        (d['r'], d['g'], d['b']) = rgbof(d['Hue'], d['Saturation'], d['Brightness']) #update r g b values
        post({'r': d['r']*d['On'], 'g': d['g']*['On'], 'b': d['b']*d['On']}) #multiplie with on state to turn light off
