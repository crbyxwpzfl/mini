



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

def gethsv():
    response = requests.get(f'https://{privates.ip}:1926/6/ambilight/cached', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    return hsvof(json.loads(response.content)['layer1']['left']['0']) #returns dict with 'Hue' 'Saturation' 'Brightness'
    

def geton():
    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    return {json.loads(response.content)['powerstate']: 1} #returns dict with 'On' or 'Standby'


#def get(path):
#    response = requests.get(f'https://{privates.ip}:1926/6/{path}', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
#    return response.content


def post(body):
    try:
        response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, json=body)
    except requests.exceptions.ConnectionError:
        print("  ----  error connecting setting ambi ----  ")
        sys.exit()
    except requests.exceptions.Timeout:
        print("  ----  timeout error setting ambi  ----  ")
        sys.exit()


def hsvof(rgb):
    (h, s, v) = colorsys.rgb_to_hsv(rgb['r']/255, rgb['g']/255, rgb['b']/255)
    return {'Hue': int(h*360),'Saturation': int(s*100),'Brightness': int(v*100)}
    
    #return(int(h*360), int(s*100), int(v*100))

def rgbof(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(((h-7)%360)/360, math.pow((s/100),0.5), (v+1)/100)
    return(int(r*255), int(g*255), int(b*255)+1)




# logic and output

if sys.argv[1] == "Get":
    d = {'On': geton} # creates dict with 'On'
    d = d.get(sys.argv[3].strip("''"), gethsv)() #overwrites dict with 'Hue' 'Saturation' 'Brightness' or 'Standby' or 'On'
    print(d.get(sys.argv[3].strip("''"), 0))   #returns value of 'characteristic' or 1 



d = {'On': geton} # creates dict with 'On'
d = d.get(sys.argv[3].strip("''"), gethsv)() #overwrites dict with 'Hue' 'Saturation' 'Brightness' or 'Standby' or 'On'
if sys.argv[1] == "Set" and geton()['Standby'] == 1: #only if tv is off
    


    d = geton() #creates dict with 'On' or 'Standby'
    if d.get('On') == None: # only if tv is off
        d.update(gethsv()) #adds 'Hue' 'Saturation' 'Brightness'
        d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    #update value of 'characteristic' or creates 'On' with value
        (d['r'], d['g'], d['b']) = rgbof(d['Hue'], d['Saturation'], d['Brightness']) #update 'r' 'g' 'b' values
        post({'r': d['r']*d['On'], 'g': d['g']*d['On'], 'b': d['b']*d['On']}) #multiplie with 'on' to turn lights off


#    d = {json.loads(get('powerstate'))['powerstate']: 1} #creates dict with 'On' or 'Standby'
#    if d.get('On') == None: # only if tv is off
#        d.update(json.loads(get('ambilight/cached'))['layer1']['left']['0']) #adds 'r' 'g' 'b'
#        (d['Hue'], d['Saturation'], d['Brightness']) = hsvof(d['r'], d['g'], d['b']) #adds 'Hue' 'Saturation' 'Brightness' 
#        d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    #update value of 'characteristic' or creates 'On' with value
#        (d['r'], d['g'], d['b']) = rgbof(d['Hue'], d['Saturation'], d['Brightness']) #update 'r' 'g' 'b' values
#        post({'r': d['r']*d['On'], 'g': d['g']*d['On'], 'b': d['b']*d['On']}) #multiplie with 'on' to turn lights off

    
    if d.get('On') == 1: # only if tv is on
