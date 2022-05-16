
import sys
sys.path.append('/Users/mini/Downloads/private/')
import privates

#from __future__ import unicode_literals
#from types import DynamicClassAttribute
#from distutils.dir_util import copy_tree
#from pathlib import Path
import pathlib
import re
import subprocess
import os
import requests
import shutil


def sub(cmdstring): # string here because shell true because only way of chaning commands
    p = subprocess.Popen(cmdstring , text=False, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout: print(line.decode()) # print line makes me wait until completion

def primedir(at):
    Path(os.path.join(d['puthere'], at)).mkdir(parents=True, exist_ok=True)    #make dir if not exsits
    #files = os.listdir(os.path.join(d['puthere'], at))    #prepend tmp to all files names
    # TODO is this neccesarry if files:   #if files exist
    for files in os.listdir(os.path.join(d['puthere'], at)):
        os.replace(os.path.join(d['puthere'], at, files), os.path.join(clonehere, at, f"tmp-{files}"))

def deltemp(at):
    for p in Path(os.path.join(clonehere, at)).glob("tmp*"):    #delete tmp dirs
        shutil.rmtree(p)


def pluses(): # TODO debug

        primedir('gists')
        response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists
        for i in response.json():
            foldername = i.get('description', " ")
            for items in i['files']: 
                foldername += i['files'][x]['filename'].replace(".", "-") + " "

            sub(['git', 'clone', i['git_pull_url'], os.path.join(clonehere, 'gists', foldername)])    #add [, '--quiet'] to shut up    
        deltemp('gists')
        sub(['osascript', '-e', f'tell application "Messages" to send "cloned gists" to participant "{phonenr}"'])


def clone():
    sub(f"plutil -convert xml1 -o {os.path.join(d['puthere'], 'transfer', 'reposetories', 'ff', 'bookmarks.xml')} {os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')}") # puts bookmarks into ff
    sub(f"git -C {os.path.join(d['puthere'], 'transfer', 'reposetories', 'ff')} commit -am \"bookmarks update\" ; " + d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories', 'ff')} push ;") # commit -am does not picup on newly created files

    for r in d['repos']: # clone repos
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git")
    
    for r in d['repos']: # pull repos
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'],'reposetories', r)} pull") # TODO gets changes from remote add --quiet to shut up 

    primedir('gists')
    response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists

    for  in response.json():
            if i['description']:    #use description as name or else chain file names
                foldername = i['description']
            else:
                foldername = ""
                for x in i['files']:
                    foldername += i['files'][x]['filename'].replace(".", "-") + " "

            sub(['git', 'clone', i['git_pull_url'], os.path.join(clonehere, 'gists', foldername)])    #add [, '--quiet'] to shut up
    
        deltemp('gists')
        sub(['osascript', '-e', f'tell application "Messages" to send "cloned gists" to participant "{phonenr}"'])

    if a in ['cr', '-cr', 'clonerepos', '-clonerepos']:   #slow but works fuck it
        primedir('reposetories')

        downedrepos = " "
        for r in repos:
            sub(['git', '-C', os.path.join(clonehere, 'reposetories'),'-c', f"core.sshCommand=\"\"ssh -i {sshpriv}\"\"", 'clone', f'git@github.com:crbyxwpzfl/{r}.git'])     #add [, '--quiet'] to shut up 
            downedrepos += r + " "
  
        deltemp('reposetories')
        sub(['osascript', '-e', f'tell application "Messages" to send "pulled {downedrepos}" to participant "{phonenr}"'])




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

    -co    converts {currentdir}/*.mkv to mp4
           converts {currentdir}/mp3*  to mp3
    
    -cl    pushes bookmarks into d['puthere']reposetories/ff/bookmarks.xml     ! clean readlist
           clones gists to d['puthere']gists/
           clones or pulls d['repos'] to d['puthere']reposetories/

    ''')

d = {'-co': convert, '-cl': 'clone',
    'puthere': '/Users/mini/Downloads/transfer/', # put d['puthere']/reposetories  d['puthere']/gists  d['puthere']/reposetories/ff/xmlbookmarks here
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned or pulled
    'currnetdir': os.getcwd() #current dir for converting stuff
    'phonenr': privates.phone    #for imessage update
    'gitcssh': f"git -c core.sshCommand=\"ssh -i {privates.opensshpriv}\"", # for clone pull psuh
    # make sure ffmpeg is in /usr/local/bin to be accesible via terminal
}

d.get(sys.argv[1].strip("''"), helps)() # call arg() or help()