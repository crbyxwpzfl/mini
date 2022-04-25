
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

def Get():
    reference()
    print(d.get(sys.argv[3].strip("''"), int(d['Brightness']/d['Brightness']) if d['Brightness'] else 0 ))    # prints 'characteristic' or calculates 'On'

def Set():
    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    reference() if json.loads(response.content)['powerstate'] == 'Standby' and sys.argv[3].strip("''") != 'On' else sys.exit()    # only when standby and ignore 'On' so only 'Brightness' causes on/offs
    d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    # update 'characteristic' value
    (r, g, b) = colorsys.hsv_to_rgb(((d['Hue']-7)%360)/360, math.pow((d['Saturation']/100),0.5), (d['Brightness'])/100)    # including Hue shift and Saturation boost
    response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, json={'r': int(r*255),'g': int(g*255),'b': int(b*255)})

def reference():
    response = requests.get(f'https://{privates.ip}:1926/6/ambilight/cached', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    d.update( json.loads(response.content)['layer1']['left']['0'] )    # adds 'r' 'g' 'b'
    (h, s, v) = colorsys.rgb_to_hsv(d['r']/255, d['g']/255, d['b']/255)    
    d.update({'Hue': int(h*360),'Saturation': int(s*100),'Brightness': int(v*100)})    # adds 'Hue' 'Saturation' 'Brightness'

d = {'Set': Set, 'Get': Get}
d.get(sys.argv[1].strip("''"))()