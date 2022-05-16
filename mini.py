
import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates

#from __future__ import unicode_literals
#from types import DynamicClassAttribute
#from distutils.dir_util import copy_tree
from pathlib import Path
import pathlib
import re
import subprocess
import os
import requests


def sub(cmdstring): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout: print(line.decode()) # print line makes me wait until completion

def primedir(at):
    Path(os.path.join(d['puthere'], at)).mkdir(parents=True, exist_ok=True)    #make dir if not exsits
    #files = os.listdir(os.path.join(d['puthere'], at))    #prepend tmp to all files names
    # TODO is this neccesarry if files:   #if files exist
    for files in os.listdir(os.path.join(d['puthere'], at)):
        os.replace(os.path.join(d['puthere'], at, files), os.path.join(d['puthere'], at, f"tmp-{files}"))

def deltemp(at):
    for p in Path(os.path.join(d['puthere'], at)).glob("tmp*"):    #delete tmp dirs
        sub(f"rm -r -f {p}")


for p in Path(os.path.join(d['puthere'], at)).glob("tmp*"):    #delete tmp dirs
    print(p)


def clone():
    sub(f"plutil -convert xml1 -o {os.path.join(d['puthere'], 'reposetories', 'ff', 'bookmarks.xml')} {os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')}") # puts bookmarks into ff
    sub(f"git -C {os.path.join(d['puthere'], 'reposetories', 'ff')} commit -am \"bookmarks update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'ff')} push ;") # commit -am does not picup on newly created files

    for r in d['repos']: # clone repos
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git")
    for r in d['repos']: # pull repos
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'],'reposetories', r)} pull") # TODO gets changes from remote add --quiet to shut up 

    primedir('gists')
    response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists

    for gist in response.json(): # use desription or all filenames as filename
        foldername = gist.get('description', "-")
        if foldername == "-":
            for f in gist['files']:
                foldername += gist['files'][f]['filename'].replace(".", "-") + "-"
        sub(f"git clone {gist['git_pull_url']} {os.path.join(d['puthere'], 'gists', foldername.replace(' ', '-'))}") # add --quiet to shut up

    #deltemp('gists')
    sub(f"osascript -e 'tell application \"Messages\" to send \"pushed bookmarks pulled repos and gists\" to participant \"{d['phonenr']}\"'")


def convert():

        if a in ['co', '-co', 'convert', '-convert']:
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
    
    -cl    pushes bookmarks into {d['puthere']}reposetories/ff/bookmarks.xml     ! clean readlist
           clones gists to {d['puthere']}gists/
           clones or pulls {d['repos']} to {d['puthere']}reposetories/

    ''')

d = {'-co': convert, '-cl': clone,
    'puthere': '/Users/mini/Downloads/transfer/', # put d['puthere']/reposetories  d['puthere']/gists  d['puthere']/reposetories/ff/xmlbookmarks here
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned or pulled
    'currentdir': os.getcwd(), #current dir for converting stuff
    'phonenr': privates.phone,    #for imessage update
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    # make sure ffmpeg is in /usr/local/bin to be accesible via terminal
}

d.get(sys.argv[1].strip("''"), helps)() # call arg() or help()