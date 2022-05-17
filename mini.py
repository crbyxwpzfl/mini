
import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates
import pathlib
import subprocess
import os
import requests


def sub(cmdstring): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout: print(line.decode()) # print line makes me wait until completion

def clone(): # clones or pulls all repos in 'toclone' and gists form github
    sub(f"plutil -convert xml1 -o {os.path.join(d['puthere'], 'transfer', 'reposetories', 'ff', 'bookmarks.xml')} {os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')}") # puts bookmarks into ff
    sub(f"git -C {os.path.join(d['puthere'], 'transfer', 'reposetories', 'ff')} commit -am \"bookmarks update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'transfer', 'reposetories', 'ff')} push ;") # commit -am does not picup on newly created files

    response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists
    for gist in response.json(): # use desription or all filenames as filename
        foldername = gist.get('description', "-")
        if foldername == "-":
            for f in gist['files']:
                foldername += gist['files'][f]['filename'].replace(".", "-") + "-"
        d['toclone'].append(['gists' , foldername.replace(' ', '-'), gist['git_pull_url']])

    for l in d['toclone']: # clone gists
        sub(d['gitcssh'] + f" clone {l[2]} {os.path.join(d['puthere'], 'transfer', l[0], l[1])}")
    for l in d['toclone']: # pull gists
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'transfer', l[0], l[1])} pull") # TODO gets changes from remote add --quiet to shut up 
    

def convert():

for path, subdirs, files in os.walk(pathlib.PurePath(d['puthere'], 'temps')):
    for name in [f for f in files if f.endswith(".mkv")]:
        print(pathlib.PurePath(path, name))

        print(pathlib.PurePath(path, name))



for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".log")]:
        print os.path.join(dirpath, filename)

import os
import os.path

for dirpath, dirnames, filenames in os.walk("."):
    for filename in [f for f in filenames if f.endswith(".log")]:
        print os.path.join(dirpath, filename)

for path, subdirs, files in os.walk(pathlib.PurePath('/Users/mini/Downloads/', 'temps')):
    for name in [f for f in files if f.endswith(".mkv")]:
        print(pathlib.PurePath(path, name))


            for f in Path(currentdir).glob("[!mp3]*.mkv"):    #convert mkvs to mp4 handbrakeCLI in downloads folder is requird
                outfile = str(f)[:-4]+".mp4"
                sub([handbrakedir, '-i', f"{f}", '-o', outfile])
                sub(['osascript', '-e', f'tell application "Messages" to send "converted {outfile}" to participant "{phonenr}"'])

        for f in Path(currentdir).glob("mp3*"):    #convert to mp3 ffmpeg in downloads folder is required
            outfile = str(f)[:-4]+".mp3"
            sub([ffmpegdir, '-i', f, outfile])
            sub(['osascript', '-e', f'tell application "Messages" to send "converted {outfile}" to participant "{phonenr}"'])

        response = requests.get('http://localhost:8080/motion?mini')


def helps():
    print(f'''

    -co    converts {d['currentdir']}/*.mkv to mp4
           converts {d['currentdir']}/mp3*  to mp3
    
    -cl    pushes bookmarks into {d['puthere']}'transfer/reposetories/ff/bookmarks.xml     ! clean readlist
           clones gists to {d['puthere']}transfer/gists/
           clones or pulls {d['toclone']}

    ''')

d = {'-co': convert, '-cl': clone,
    'puthere': '/Users/mini/Downloads/', # put d['puthere']/reposetories  d['puthere']/gists  d['puthere']/reposetories/ff/xmlbookmarks here
    'toclone': [['reposetories', 'private', 'git@github.com:crbyxwpzfl/private.git'], ['reposetories', 'mini', 'git@github.com:crbyxwpzfl/mini.git'], ['reposetories', 'ff', 'git@github.com:crbyxwpzfl/ff.git'], ['reposetories', 'spinala', 'git@github.com:crbyxwpzfl/spinala.git'], ['reposetories', 'rogflow', 'git@github.com:crbyxwpzfl/rogflow.git'], ['reposetories', 'crbyxwpzfl', 'git@github.com:crbyxwpzfl/crbyxwpzfl.git']],
    'currentdir': os.getcwd(), #current dir for converting stuff
    'phonenr': privates.phone, #for imessage update
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    # make sure ffmpeg is in /usr/local/bin to be accesible via terminal
}

d.get(sys.argv[1].strip("''"), helps)() # call arg() or help()