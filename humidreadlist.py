#let the cluster fuck begin

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates

import os

import subprocess


def Get():
    print(dict.get(sys.argv[3].strip("''") , 1))
    sys.exit()

def run(cmdstring): # string here because shell true because only way of chaning commands
    lines = subprocess.run(cmdstring , text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #print(lines.stdout)
    return lines.stdout


def overwritesite():
    fuckedlist = run(d['sshpi'] + "nordvpn status")[12:].strip('\n').split('\n') # clean up output and add to dict
    for count, elem in enumerate(fuckedlist): d[fuckedlist[count].split(': ')[0]] = fuckedlist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value
    d['ccode'] = d.get('Current server', "de")[:2] # insert tihs into calss selector
    d['color'] = "#5cf287" if d['Status'] == 'Connected' else "#fc4444" # insert this into color
    with open(d['site'], 'r+') as f:
        lines = f.readlines()
        lines[6] = f"path.{d['ccode']} {{fill: {d['color']};}}  /* set color and ccode according to on off state */\n"
        lines[7] = f"path.{d['ccode']}:hover {{stroke: {d['color']}; stroke-width: 4; fill: {d['color']};}}\n"
        print(lines[6])
        print(lines[7])
        f.seek(0)
        print(lines)
        f.writelines(lines)

        lines[6] = f"path.{d['ccode']} {{fill: {d['color']};}}  /* set color and ccode according to on off state */\n"
        lines[7] = f"path.{d['ccode']}:hover {{stroke: {d['color']}; stroke-width: 4; fill: {d['color']};}}\n"


def pushsite():
    for r in d['repos']:
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git") # TODO move this to setup function
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', r)} pull") # gets changes from remote add --quiet to shut up
        d['message']+= r + " "
    #if all up to date
    #change file now
    run(f"git -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} commit -am \"site update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} push" ) # commit -am does not picup on new created files
    run(f"osascript -e tell application \"Messages\" to send \"site updated and pulled {message}\" to participant \"{d['phonenr']}\"") # send message site updated



d = {'Get': Get, # defs for running directly in cli via arguments
    'CurrentRelativeHumidity': 80, 'StatusActive': 1, 'StatusTampered': 0, # for homebridge
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned
    'puthere': '/Users/mini/Downloads/transfer/', # #put ./repos ./gists ./repos/ff/xmlbookmarks ./repos/ff/dwl-archive here
    'message': " ", # message to send
    'phonenr': privates.phone,
    'site': "/Users/mini/Desktop/indexcopy.txt",
}
dict.get(sys.argv[1].strip("''"), sys.exit)() # call 'Get' or sys exit()