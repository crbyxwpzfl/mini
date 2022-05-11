#let the cluster fuck begin

import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
import os
import subprocess
import fileinput # for overwritesite()
import plistlib # for parsereadlist()

def Get():
    print(dict.get(sys.argv[3].strip("''") , 1))
    sys.exit()

def run(cmdstring): # string here because shell true because only way of chaning commands
    process = subprocess.run(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(process.stdout.decode())
    return process.stdout.decode()

def parsereadlist():
    run(f"plutil -convert xml1 -o {d['bookmarksxml']} {d['bookmarksplist']}") # TODO move this to setup/backup function
    plist = plistlib.load(open(d['bookmarksplist'], 'rb'))
    for child in plist['Children']:
        if child.get('Title', None) == 'com.apple.ReadingList':
            for item in child['Children']:
                print(item['URIDictionary']['title'])
                print(item['URLString'])
                if not item['URLString'].startswith('https://'): d['ariaurls'][item['URIDictionary']['title']] = item['URLString'] # all not https into aria
                if item['URLString'].startswith('https://') and not item['URIDictionary']['title'].startswith('vpn '): d['dlpurls'][item['URIDictionary']['title']] = item['URLString'] # all https and not vpn to into dlp
                if item['URLString'].startswith('https://') and item['URIDictionary']['title'].startswith('vpn '): d['vpnto'] = "connect " + item['URLString'][-2:] # vpn to country into d 'vpnto'

def vpnstatus(): # pipe vpn status into dict
    nicelist = run(d['sshpi'] + "nordvpn status").lstrip('\r-\r  \r\r-\r  \r').rstrip('\n').split('\n') # get vpn status and clean up output a bit
    for count, elem in enumerate(nicelist): d[nicelist[count].split(': ')[0]] = nicelist[count].split(':')[1].strip() # for each elem split elem by : then add first elem of split as key and second as value to dict

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

def setvpn():
    run(d['sshpi']  + "nordvpn " + d.get('vpnto', "disconnect"))
    pushsite() # only depends on vpn status() not parrsereadlist()

def head():
    parsereadlist() # to get desired vpn location and urls
    setvpn() # set vpn to location and psuhsite()
    
    #if sth to download for aria or dlp and vpn is ok
        #aria() or dlp()


    #run(f"osascript -e 'tell application \"Messages\" to send \"site updated and pulled {d['message']}\" to participant \"{d['phonenr']}\"'") # send message site updated


d = {'test': head, 'Get': Get, # defs for running directly in cli via arguments
    'CurrentRelativeHumidity': 80, 'StatusActive': 1, 'StatusTampered': 0, # for homebridge
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    'sshpi': f"ssh {privates.piaddress} -i {privates.opensshpriv} ", # attentione to the last space
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned
    'puthere': '/Users/mini/Downloads/transfer/', # #put ./repos ./gists ./repos/ff/xmlbookmarks ./repos/ff/dwl-archive here
    'message': " ", # message to send
    'phonenr': privates.phone,
    'bookmarksxml': "/Users/mini/Desktop/SafariBookmarks.xml", # where to export bookmarks to
    'bookmarksplist': os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist'), # where apple stores bookmarks plist 
    'ariaurls': {},
    'dlpurls': {},
}
d.get(sys.argv[1].strip("''"), sys.exit)() # call 'Get' or sys exit()