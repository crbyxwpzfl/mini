



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

#def gethsv():
#   response = requests.get(f'https://{privates.ip}:1926/6/ambilight/cached', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
#   return hsvof(json.loads(response.content)['layer1']['left']['0']) #returns dict with 'Hue' 'Saturation' 'Brightness'
    

#def geton():
#    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
#    return {json.loads(response.content)['powerstate']: 1} #returns dict with 'On' or 'Standby'


#def get(path):
#    response = requests.get(f'https://{privates.ip}:1926/6/{path}', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
#    return response.content



#def post():
#    d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''")) #update value of 'characteristic'
#    calculatergb()
#    try:
#       response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, json={'r': d['r'],'g': d['g'],'b': d['b']})
#        print(response.content)
#    except requests.exceptions.ConnectionError:
#        print("  ----  error connecting setting ambi ----  ")
#        sys.exit()
#    except requests.exceptions.Timeout:
#        print("  ----  timeout error setting ambi  ----  ")
#        sys.exit()

#def powerstate():
#    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
#    hsv() if json.loads(response.content)['powerstate'] == 'Standby' else sys.exit()
    #d.pop(json.loads(response.content)['powerstate']) #deletes 'On' or 'Standby'
    #d.update( {json.loads(response.content)['powerstate']: = 1} )

def Get():
    d.get(sys.argv[3].strip("''"))()
    print(d.get(sys.argv[3].strip("''")))

def Set():
    response = requests.get(f'https://{privates.ip}:1926/6/powerstate', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    hsv() if json.loads(response.content)['powerstate'] == 'Standby' else sys.exit()    #only when standby
    d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''")) #update value of 'characteristic'
    calculatergb()
    response = requests.post(f'http://{privates.ip}:1925/6/ambilight/cached', timeout=2, json={'r': d['r'],'g': d['g'],'b': d['b']})

def hsv():
    response = requests.get(f'https://{privates.ip}:1926/6/ambilight/cached', timeout=2, verify=False, auth=HTTPDigestAuth(privates.user, privates.pw))
    d.update( json.loads(response.content)['layer1']['left']['0'] ) #updates 'r' 'g' 'b'
    calculatehsv() #updates 'Hue' 'Saturation' 'Brightness'

def calculatehsv():
    (h, s, v) = colorsys.rgb_to_hsv(d['r']/255, d['g']/255, d['b']/255)
    d.update({'Hue': int(h*360),'Saturation': int(s*100),'Brightness': int(v*100)})

def calculatergb():
    (r, g, b) = colorsys.hsv_to_rgb(((d['Hue']-7)%360)/360, math.pow((d['Saturation']/100),0.5), (d['Brightness']+1)/100)
    d.update({'r': int(r*255),'g': int(g*255),'b': int(b*255)})

def calculateon():
    hsv()
    d.update({'On': int(d[Brightness]/d[Brightness]) if d['Brightness'] else 0})


# logic and output

d = {'Set': Set, 'Get': Get, 'On': calculateon, 'Hue': hsv,'Saturation': hsv,'Brightness': hsv}
d.get(sys.argv[1].strip("''"))()





#d = {'On': geton} # creates dict with 'On'
#d = d.get(sys.argv[3].strip("''"), gethsv)() #overwrites dict with 'Hue' 'Saturation' 'Brightness' or 'Standby' or 'On' 


#if sys.argv[1] == "Set" and d.get('Standby') == 1: #set only if tv is off
#    d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    #update value of 'characteristic'
#    post( d.get('On', rgbof(d)) )   #post 'On' will cause bad request 

#if sys.argv[1] == "Get":
#    print(d.get(sys.argv[3].strip("''"), 0))   #returns value of 'characteristic' or 0 


#if sys.argv[1] == "Get":
#    d = {'On': geton} # creates dict with 'On'
#    d = d.get(sys.argv[3].strip("''"), gethsv)() #overwrites dict with 'Hue' 'Saturation' 'Brightness' or 'Standby' or 'On'
#   print(d.get(sys.argv[3].strip("''"), 0))   #returns value of 'characteristic' or 1 
    

#if sys.argv[1] == "Set":
#    d = geton() #creates dict with 'On' or 'Standby'
#    if d.get('On') == None: # only if tv is off
#        d.update(gethsv()) #adds 'Hue' 'Saturation' 'Brightness'
#       d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    #update value of 'characteristic' or creates 'On' with value
#        (d['r'], d['g'], d['b']) = rgbof(d['Hue'], d['Saturation'], d['Brightness']) #update 'r' 'g' 'b' values
#        post({'r': d['r']*d['On'], 'g': d['g']*d['On'], 'b': d['b']*d['On']}) #multiplie with 'on' to turn lights off


#    d = {json.loads(get('powerstate'))['powerstate']: 1} #creates dict with 'On' or 'Standby'
#    if d.get('On') == None: # only if tv is off
#        d.update(json.loads(get('ambilight/cached'))['layer1']['left']['0']) #adds 'r' 'g' 'b'
#        (d['Hue'], d['Saturation'], d['Brightness']) = hsvof(d['r'], d['g'], d['b']) #adds 'Hue' 'Saturation' 'Brightness' 
#        d[sys.argv[3].strip("''")] = int(sys.argv[4].strip("''"))    #update value of 'characteristic' or creates 'On' with value
#        (d['r'], d['g'], d['b']) = rgbof(d['Hue'], d['Saturation'], d['Brightness']) #update 'r' 'g' 'b' values
#        post({'r': d['r']*d['On'], 'g': d['g']*d['On'], 'b': d['b']*d['On']}) #multiplie with 'on' to turn lights off

    
#    if d.get('On') == 1: # only if tv is on
