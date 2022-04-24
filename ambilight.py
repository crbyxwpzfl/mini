
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
    d.get(sys.argv[3].strip("''"))()
    print(d.get(sys.argv[3].strip("''")))

def Set():
    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    hsv() if json.loads(response.content)['powerstate'] == 'Standby' else sys.exit()    #only when standby
    d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''")) #update value of 'characteristic'
    calculatergb()
    if d['r'] == 0 and d['g'] == 0 and d['b'] == 0 and d['Brightness'] != 0: d['r'] = 1 #inital value issue for hsv conversion
    response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, json={'r': d['r'],'g': d['g'],'b': d['b']})

def hsv():
    response = requests.get(f'https://{privates.ip}:1926/6/ambilight/cached', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    d.update( json.loads(response.content)['layer1']['left']['0'] ) #updates 'r' 'g' 'b'
    calculatehsv() #updates 'Hue' 'Saturation' 'Brightness'

def calculatehsv():
    (h, s, v) = colorsys.rgb_to_hsv(d['r']/255, d['g']/255, d['b']/255)
    d.update({'Hue': int(h*360),'Saturation': int(s*100),'Brightness': int(v*100)})

def calculatergb():
    (r, g, b) = colorsys.hsv_to_rgb(((d['Hue']-7)%360)/360, math.pow((d['Saturation']/100),0.5), (d['Brightness'])/100) #including ue shift and Saturation boost
    d.update({'r': int(r*255),'g': int(g*255),'b': int(b*255)})

def calculateon():
    hsv()
    d.update({'On': int(d[Brightness]/d[Brightness]) if d['Brightness'] else 0})

d = {'Set': Set, 'Get': Get, 'On': calculateon, 'Hue': hsv,'Saturation': hsv,'Brightness': hsv}
d.get(sys.argv[1].strip("''"))()
