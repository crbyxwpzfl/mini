from __future__ import unicode_literals
import sys
import re
import subprocess
import os
import requests

#sys.path.append(os.environ.get('privates'))
# import privates for phone number and path to open ssh key 
sys.path.append('/Users/mini/private/')
import privates

#set download dir
dir = "/Volumes/transfer/"




# PULL READ LIST
import youtube_dl

#logger to quiet output
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

#send a message with filename to confirm downlad
def my_hook(d):
    if d['status'] == 'finished':
        #print(d['filename'])
        filename = d['filename'][22:]
        output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, filename], stdout=subprocess.PIPE)

#set ytdl options
ydl_opts = {
    'simulate': False,
    'restrict-filenames': False,
    'ignoreerrors': True,
    'download_archive': os.path.join(dir, 'see', 'archive.txt'),
    'outtmpl': os.path.join(dir, 'see', '%(title)s.%(ext)s'),
    'progress_hooks': [my_hook],
    'logger': MyLogger(),
}

#convert bookmark plist to xml
output = subprocess.Popen(['plutil', '-convert', 'xml1', '-o', os.path.join(dir, 'see', 'SafariBookmarks.xml'), '/Users/mini/Library/Safari/Bookmarks.plist'], stdout=subprocess.PIPE)
#print (output.stdout.read())

#read xml into variable file
file = open(os.path.join(dir, 'see', 'SafariBookmarks.xml'), "r")

#dirty but works to find readinglist urls
for line in file:
    if re.search("^					<string>http", line):
        
        #downlad url content
        #print (line[13:-10])
        url = line[13:-10]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])





# GITHUB GISTS BACKUP

#make dir if not exsits
from pathlib import Path
Path(os.path.join(dir, 'github-gists')).mkdir(parents=True, exist_ok=True)

#append tmp to all files names 
files = os.listdir(os.path.join(dir, 'github-gists'))
for f in files:
    os.replace(os.path.join(dir, 'github-gists', f), os.path.join(dir, 'github-gists', f"tmp-{f}"))

#get all gists
response = requests.get('https://api.github.com/users/crbyxwpzfl/gists')

for i in response.json():
    #gets names of all files inside gist
    if i['description']
        foldername = i['description']
    else
        foldername = ""
        for x in i['files']:
            foldername += i['files'][x]['filename'].replace(".", "-") + " "
        #print(foldername)

    #pull this url
    #print(i['git_pull_url'])
    output = subprocess.Popen(['git', 'clone', i['git_pull_url'], os.path.join(dir, 'github-gists', foldername)], stdout=subprocess.PIPE)

#delete tmp dirs
import shutil
for p in Path(os.path.join(dir, 'github-gists')).glob("tmp*"):
    shutil.rmtree(p)

output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privates.phone, "cloned gists"], stdout=subprocess.PIPE)



# GITHUB REPOS BACKUP

#make dir if not exsits
from pathlib import Path
Path(os.path.join(dir, 'github-repos')).mkdir(parents=True, exist_ok=True)

#append tmp to all files names 
files = os.listdir(os.path.join(dir, 'github-repos'))
for f in files:
    os.replace(os.path.join(dir, 'github-repos', f), os.path.join(dir, 'github-repos', f"tmp-{f}"))

output = subprocess.run(['git', 'clone', 'git@github.com:crbyxwpzfl/private.git','-c', 'user.name="crbyxwpzfl"', '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", os.path.join(dir, 'github-repos', 'private')], stdout=subprocess.PIPE)
output = subprocess.run(['git', 'clone', 'git@github.com:crbyxwpzfl/mini.git','-c', 'user.name="crbyxwpzfl"', '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", os.path.join(dir, 'github-repos', 'mini')], stdout=subprocess.PIPE)
output = subprocess.run(['git', 'clone', 'git@github.com:crbyxwpzfl/ff.git','-c', 'user.name="crbyxwpzfl"', '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", os.path.join(dir, 'github-repos', 'ff')], stdout=subprocess.PIPE)
output = subprocess.run(['git', 'clone', 'git@github.com:crbyxwpzfl/spinala.git','-c', 'user.name="crbyxwpzfl"', '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", os.path.join(dir, 'github-repos', 'spinala')], stdout=subprocess.PIPE)
output = subprocess.run(['git', 'clone', 'git@github.com:crbyxwpzfl/rogflow.git','-c', 'user.name="crbyxwpzfl"', '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", os.path.join(dir, 'github-repos', 'rogflow')], stdout=subprocess.PIPE)
output = subprocess.run(['git', 'clone', 'git@github.com:crbyxwpzfl/crbyxwpzfl.git','-c', 'user.name="crbyxwpzfl"', '-c', f"core.sshCommand=\"\"ssh -i {privates.opensshpriv}\"\"", os.path.join(dir, 'github-repos', 'crbyxwpzfl')], stdout=subprocess.PIPE)

#delete tmp dirs
import shutil
for p in Path(os.path.join(dir, 'github-repos')).glob("tmp*"):
    shutil.rmtree(p)

output = subprocess.Popen(['osascript', '/Users/mini/mini/sendMessage.applescript', privats.phone, "cloned repos"], stdout=subprocess.PIPE)