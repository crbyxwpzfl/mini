#let the cluster fuck begin

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
import os
import subprocess
import fileinput # for overwritesite()

def Get():
    print(dict.get(sys.argv[3].strip("''") , 1))
    sys.exit()

def run(cmdstring): # string here because shell true because only way of chaning commands
    lines = subprocess.run(cmdstring , text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(lines.stdout)
    return lines.stdout

def vpnstatus(): # pipe vpn status into dict
    fuckedlist = run(d['sshpi'] + "nordvpn status")[12:].strip('\n').split('\n') # get vpn status and clean up output a bit
    for count, elem in enumerate(fuckedlist): d[fuckedlist[count].split(': ')[0]] = fuckedlist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value to dict

def overwritesite(): # rewrite site content corrosponding to vpnstatus()
    vpnstatus()
    d['ccode'] = d.get('Current server', "de")[:2] # get country then insert country code into css calss selector
    d['color'] = "#5cf287" if d['Status'] == 'Connected' else "#fc4444" # get on off color insert color part of css class selector
    d['line7'] = f"path.{d['ccode']} {{fill: {d['color']};}}  /* set color and ccode according to on off state */\n" # construct linnes
    d['line8'] = f"path.{d['ccode']}:hover {{stroke: {d['color']}; stroke-width: 4; fill: {d['color']};}}\n"
    for line in fileinput.input([os.path.join(d['puthere'], 'reposetories', 'spinala', 'index.html')], inplace=True): # open file and overwrite lines
        print(d['line7'], end='') if fileinput.filelineno() == 7 else print(d['line8'], end='') if fileinput.filelineno() == 8 else print(line, end='')

def pushsite(): # pull all repos and push changes of overwritesite()
    for r in d['repos']:
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git") # TODO move this to setup function
        run(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', r)} pull") # gets changes from remote add --quiet to shut up
        d['message']+= r + " "
    overwritesite() # update site content
    run(f"git -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} commit -am \"site update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'spinala')} push ;" ) # commit -am does not picup on new created files


def parsereadlist():
    print("todo")

def head():
    pushsite()
    #parse readlist()
    #aria run()
    #dpl run()
    run(f"osascript -e 'tell application \"Messages\" to send \"site updated and pulled {d['message']}\" to participant \"{d['phonenr']}\"'") # send message site updated
    sys.exit()


d = {'head': head, 'Get': Get, # defs for running directly in cli via arguments
    'CurrentRelativeHumidity': 80, 'StatusActive': 1, 'StatusTampered': 0, # for homebridge
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned
    'puthere': '/Users/mini/Downloads/transfer/', # #put ./repos ./gists ./repos/ff/xmlbookmarks ./repos/ff/dwl-archive here
    'message': " ", # message to send
    'phonenr': privates.phone,
}
d.get(sys.argv[1].strip("''"), sys.exit)() # call 'Get' or sys exit()