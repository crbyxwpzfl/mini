from __future__ import unicode_literals
import sys
import re
import subprocess
import os
from os.path import expanduser

#set dir
dir = expanduser("~")+"/Library/Mobile Documents/com~apple~CloudDocs/"

#import ytdl via path
sys.path.append("/usr/local/bin/youtube-dl")
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
        print(d['filename'])
        filename = d['filename'][20:]
        output = subprocess.Popen(['osascript', os.path.join(dir, 'sendMessage.applescrip'), 'hardcodedinscript', filename], stdout=subprocess.PIPE)

#set ytdl options
ydl_opts = {
    'simulate': False,
    'restrict-filenames': False,
    'ignoreerrors': True,
    'download_archive': os.path.join(dir, 'archive.txt'),
    'outtmpl': os.path.join(dir, '%(title)s.%(ext)s'),
    'progress_hooks': [my_hook],
    'logger': MyLogger(),
}

#convert bookmark plist to xml
output = subprocess.Popen(['plutil', '-convert', 'xml1', '-o', os.path.join(dir, 'SafariBookmarks.xml'), '/Users/mini/Library/Safari/Bookmarks.plist'], stdout=subprocess.PIPE)
#print (output.stdout.read())

#read xml into var file
file = open("/Users/mini/Desktop/SafariBookmarks.xml", "r")

#dirty but works to find readinglist urls
for line in file:
    if re.search("^					<string>http", line):
        
        #downlad url content
        #print (line[13:-10])
        url = line[13:-10]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])