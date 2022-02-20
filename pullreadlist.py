privdir = '/Users/mini/private/'
sys.path.append(privdir)
import privates

from types import DynamicClassAttribute
from pathlib import Path
import sys
import re
import subprocess
import os
import requests
import pathlib
import shutil

currentdir = os.getcwd()    #current dir dir to put /dir/gists /dir/reposetories
phonenr = privates.phone    #for imessage update
sshpriv = privates.opensshpriv  #for clone repos
handbrakedir = '/Users/mini/Downloads/HandBrakeCLI' #for mp4 converting 
ffmpegdir = '/Users/mini/Downloads/ffmpeg'  #for mp3 converting

bookmarksxml = os.path.join(privdir, 'SafariBookmarks.xml')
bookmarksplist = os.path.join(os.environ.get('HOME'), 'Library', 'Safari', 'Bookmarks.plist')

ydlopts = {    #set ytdl options
    'simulate': False,
    'restrict-filenames': False,
    'ignoreerrors': True,
    'download_archive': os.path.join(privdir, 'readlist-archive.txt'),   #use archive in priv dir
    'outtmpl': os.path.join(currentdir, 'readlist', '%(id)s-%(title).50s.%(ext)s'),
    'progress_hooks': [hook],
    'logger': Logger(),
}

class Logger(object):    #logger for ytdl pass instead of print(msg) to quiet output
    def debug(self, msg):
        print(msg)
    def warning(self, msg):
        print(msg)
    def error(self, msg):
        print(msg)

def sub(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line)

def primedir(at):
    Path(os.path.join(currentdir, at)).mkdir(parents=True, exist_ok=True)    #make dir if not exsits

    files = os.listdir(os.path.join(currentdir, at))    #prepend tmp to all files names
    if files:   #if files exist
        for f in files:
            os.replace(os.path.join(currentdir, at, f), os.path.join(currentdir, at, f"tmp-{f}"))

def deltemp(at):
    for p in Path(os.path.join(dicurrentdir, at)).glob("tmp*"):    #delete tmp dirs
        shutil.rmtree(p)

def hook(d):    #send a message with filename to confirm ytdl downlad 
    if d['status'] == 'finished':
        filename = d['filename'][22:]
        sub(['osascript', '-e', f'tell application "Messages" to send "{filename}" to participant "{phonenr}"'])


for a in sys.argv:
    if a in ['pr', '-pr', 'pullreadlist', '-pullreadlist']:
        from __future__ import unicode_literals
        import youtube_dl

        Path(os.path.join(currentdir, 'readlist')).mkdir(parents=True, exist_ok=True)    #make dir if not exsits

        sub(['plutil', '-convert', 'xml1', '-o', bookmarksxml, bookmarksplist])     #convert bookmark plist to xml

        file = open(bookmarksxml, "r")   #read xml into variable file
        for line in file:                #dirty but works to find readinglist urls
            if re.search("^					<string>http", line):
                url = line[13:-10]
                with youtube_dl.YoutubeDL(ydlopts) as ydl:
                    ydl.download([url])


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

            sub(['git', 'clone', i['git_pull_url'], os.path.join(currentdir, 'gists', foldername)])    #add [, '--quiet'] to shut up
    
        deltemp('gists')
        sub(['osascript', '-e', f'tell application "Messages" to send "cloned gists" to participant "{phonenr}"'])



    if a in ['cr', '-cr', 'clonerepos', '-clonerepos']:   #slow but works fuck it
        primedir('reposetories')

        downedrepos = " "
        repos = ["private", "mini", "ff", "spinala", "rogflow", "crbyxwpzfl"]
        for r in repos:
            sub(['git', '-C', os.path.join(currentdir, 'reposetories'),'-c', f"core.sshCommand=\"\"ssh -i {sshpriv}\"\"", 'clone', f'git@github.com:crbyxwpzfl/{r}.git'])     #add [, '--quiet'] to shut up 
            downedrepos += r + " "
  
        deltemp('reposetories')
        sub(['osascript', '-e', f'tell application "Messages" to send "pulled {downedrepos}" to participant "{phonenr}"'])



print ("")
print ("currently in")
print (f"    {currentdir}")
print ("avalible flags")
print (f"    -pr -pullreadlist     pulls readlist to {currentdir}")
print (f"    -co -convert          converts {currentdir}/*.mkv to mp4 and {currentdir}/mp3* to mp3")
print (f"    -cg -clonegists       clones gists to {currentdir}/gists")
print (f"    -cr -clonerepos       pulls reposetories to {currentdir}/reposetories")
print ("")