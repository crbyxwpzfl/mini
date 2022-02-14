from __future__ import unicode_literals
import sys
import re
import subprocess
import os
import requests
from pathlib import Path
import pathlib
import shutil

import youtube_dl

#sys.path.append(os.environ.get('privates'))
# import privates for phone number and /path/to/open ssh key 
sys.path.append('/Users/mini/private/')
import privates

global dir 
dir = "/Volumes/transfer/"    #dir with /dir/gists /dir/reposetories and 
    

def pullreadlist():
    class MyLogger(object):    #logger pass to quiet output
        def debug(self, msg):
            print(msg)
        def warning(self, msg):
            print(msg)
        def error(self, msg):
            print(msg)

    def my_hook(d):    #send a message with filename to confirm downlad
        if d['status'] == 'finished':
            #print(d['filename'])
            filename = d['filename'][22:]
            output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, filename], stdout=subprocess.PIPE)

    ydl_opts = {    #set ytdl options
        'simulate': False,
        'restrict-filenames': False,
        'ignoreerrors': True,
        'download_archive': os.path.join(dir, 'readlist', 'archive.txt'),
        'outtmpl': os.path.join(dir, 'readlist', '%(id)s-%(title).50s.%(ext)s'),
        'progress_hooks': [my_hook],
        'logger': MyLogger(),
    }

    #convert bookmark plist to xml
    output = subprocess.Popen(['plutil', '-convert', 'xml1', '-o', os.path.join(dir, 'readlist', 'SafariBookmarks.xml'), '/Users/mini/Library/Safari/Bookmarks.plist'], stdout=subprocess.PIPE)
    #print (output.stdout.read())

    #read xml into variable file
    file = open(os.path.join(dir, 'readlist', 'SafariBookmarks.xml'), "r")

    #dirty but works to find readinglist urls
    for line in file:
        if re.search("^					<string>http", line):
            #downlad url content
            #print (line[13:-10])
            url = line[13:-10]
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

def clonegists():
    Path(os.path.join(dir, 'gists')).mkdir(parents=True, exist_ok=True)    #make dir if not exsits
 
    files = os.listdir(os.path.join(dir, 'gists'))    #prepend tmp to all files names
    for f in files:
        os.replace(os.path.join(dir, 'gists', f), os.path.join(dir, 'gists', f"tmp-{f}"))

    response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')    #get all gists

    for i in response.json():
        if i['description']:    #use description as name or else chain file names
            foldername = i['description']
        else:
            foldername = ""
            for x in i['files']:
                foldername += i['files'][x]['filename'].replace(".", "-") + " "
            #print(foldername)

        #print(i['git_pull_url'])
        output = subprocess.Popen(['git', 'clone', i['git_pull_url'], os.path.join(dir, 'gists', foldername)], stdout=subprocess.PIPE)    #add [, '--quiet'] to shut up

    for p in Path(os.path.join(dir, 'gists')).glob("tmp*"):    #delete tmp dirs
        shutil.rmtree(p)

    output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, "cloned gists"], stdout=subprocess.PIPE)    #add [, '--quiet'] to shut up

def pullrepos():
    Path(os.path.join(dir, 'reposetories')).mkdir(parents=True, exist_ok=True)    #make dir if not exsits
    downedrepos = " "
    files = os.listdir(os.path.join(dir, 'reposetories'))    #list all files
    for f in files:
        output = subprocess.run(['git', '-C', os.path.join(dir, 'reposetories', f), 'fetch', '--all'], stdout=subprocess.PIPE)    #add [, '--quiet'] to shut up
        output = subprocess.run(['git', '-C', os.path.join(dir, 'reposetories', f), 'reset', '--hard'], stdout=subprocess.PIPE)    #add [, '--quiet'] to shut up
        output = subprocess.run(['git', '-C', os.path.join(dir, 'reposetories', f), '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", 'pull'], stdout=subprocess.PIPE)    #add [, '--quiet'] to shut up 
        downedrepos += f + " "

    output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, f"pulled {downedrepos}"], stdout=subprocess.PIPE)

def convert():
    Path(os.path.join(dir, 'readlist')).mkdir(parents=True, exist_ok=True)    #make dir if not exsits
    
    for f in Path(pathlib.Path().resolve()).glob("[!mp3]*.mkv"):    #convert mkvs to mp4 handbrakeCLI in downloads folder is requird
        outfile = str(f)[:-4]+".mp4"
        process = subprocess.Popen(['/Users/mini/Downloads/HandBrakeCLI', '-i', f"{f}", '-o', outfile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            print(line)
        output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, f"converted {outfile}"], stdout=subprocess.PIPE)


    for f in Path(pathlib.Path().resolve()).glob("mp3*"):    #convert to mp3 ffmpeg in downloads folder is required
        outfile = str(f)[:-4]+".mp3"
        process = subprocess.Popen(['/Users/mini/Downloads/ffmpeg', '-i', f, outfile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            print(line)
        output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, f"converted {outfile}"], stdout=subprocess.PIPE)


for a in sys.argv:
    if a in ['conv', '-conv', 'convert', '-convert']:
        convert()
        response = requests.get('http://localhost:8080/motion?mini')
    if a in ['prl', '-prl', 'pullreadlist', '-pullreadlist']:
        pullreadlist()
    if a in ['clg', '-clg', 'clonegists', '-clonegists']:
        clonegists()
    if a in ['pr', '-pr', 'pullrepos', '-pullrepos']:
        pullrepos()

print ("")
print ("currently in")
print (f"    {pathlib.Path().resolve()}")
print ("avalible flags")
print ("    -pullreadlist     pulls readlist to /Volumes/transfer/readlist/")
print (f"    -convert          converts {pathlib.Path().resolve()}/*.mkv to mp4 and {pathlib.Path().resolve()}/mp3* to mp3")
print ("    -clonegists       clones gists to /Volumes/transfer/gists/")
print ("    -pullrepos        pulls reposetories to /Volumes/transfer/reposetories/ ")
print ("")