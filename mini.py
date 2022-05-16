
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


def sub(cmd):
    process = subprocess.Popen(cmd, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        print(line)

        #if "fail message" in str(line):    #fallback to ffmpeg when handbrake fails
        #    print("falling back to ffmpeg")
        #    process.terminate()
        #    sub([ffmpegdir, '-y', '-i', f, outfile])


def primedir(at):
    Path(os.path.join(clonehere, at)).mkdir(parents=True, exist_ok=True)    #make dir if not exsits

    files = os.listdir(os.path.join(clonehere, at))    #prepend tmp to all files names
    if files:   #if files exist
        for f in files:
            os.replace(os.path.join(clonehere, at, f), os.path.join(clonehere, at, f"tmp-{f}"))

def deltemp(at):
    for p in Path(os.path.join(clonehere, at)).glob("tmp*"):    #delete tmp dirs
        shutil.rmtree(p)


currentdir = os.getcwd()    #current dir for converting stuff
clonehere = '/Users/mini/Downloads/transfer/'  #put ./repos ./gists ./repos/ff/xmlbookmarks ./repos/ff/dwl-archive here
phonenr = privates.phone    #for imessage update
sshpriv = privates.opensshpriv  #for clone repos
handbrakedir = '/Users/mini/Downloads/HandBrakeCLI' #for mp4 converting 
ffmpegdir = '/Users/mini/Downloads/ffmpeg'  #for mp3 converting
repos = ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"]   #repos to clone used in clonerepos def

bookmarksxml =  '/Users/mini/Downloads/SafariBookmarks.xml'    #where to export bookmarks to
bookmarksplist = os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')


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


    if a in ['cg', '-cg', 'clonegists', '-clonegists']:
        primedir('gists')

        response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists

        for i in response.json():
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


if a not in [ 'cr', '-cr', 'clonerepos', '-clonerepos',
             'cg', '-cg', 'clonegists', '-clonegists',
             'co', '-co', 'convert', '-convert',
             'pr', '-pr', 'pullreadlist', '-pullreadlist']:
    
    print(f'''

    -pr -pullreadlist   pulls readlist to {currentdir}/readlist/
    
    -co -convert        {currentdir}/*.mkv to mp4
                        {currentdir}/mp3*  to mp3
    
    -cg -clonegists     clones gists to {clonehere}gists/
    
    -cr -clonerepos     pulls reposetories to {clonehere}reposetories/
                            {repos}
    ''')


def pluses(): # TODO debug
    for r in d['repos']: # out of pushsite() TODO only pull spinala here rest perhaps in a complete back up funktion
        sub(d['gitcssh'] + f" -C {os.path.join(d['puthere'], 'reposetories')} clone git@github.com:crbyxwpzfl/{r}.git", True) # TODO move this to setup function
        print(f"cloned {r} to {os.path.join(d['puthere'], 'reposetories')}")
    
    sub(f"plutil -convert xml1 -o {os.path.join(d['puthere'], 'transfer', 'reposetories', 'ff', 'SafariBookmarks.xml')} {os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')}", True) # out of parsereadlist() TODO move this to setup function


        primedir('gists')
        response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists
        for i in response.json():
            foldername = i.get('description', " ")
            for items in i['files']: 
                foldername += i['files'][x]['filename'].replace(".", "-") + " "

            sub(['git', 'clone', i['git_pull_url'], os.path.join(clonehere, 'gists', foldername)])    #add [, '--quiet'] to shut up    
        deltemp('gists')
        sub(['osascript', '-e', f'tell application "Messages" to send "cloned gists" to participant "{phonenr}"'])


    'puthere': '/Users/mini/Downloads/', # put d['puthere']/transfer/reposetories  d['puthere']/gists  d['puthere']/transfer/reposetories/ff/xmlbookmarks  here
    'repos': ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"], # all these repos get cloned or pulled
