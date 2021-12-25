from __future__ import unicode_literals
import sys
import re
import subprocess

#import ytdl via path
sys.path.append("/usr/local/bin/youtube-dl")
import youtube_dl

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
        filename = d['filename'][20:]
        output = subprocess.Popen(['osascript', '/Users/mini/Desktop/sendMessage.applescript', 'hardcodedinscript', filename], stdout=subprocess.PIPE)

#set ytdl options
ydl_opts = {
    'simulate': False,
    'restrict-filenames': False,
    'ignoreerrors': True,
    'download_archive': '/Users/mini/Desktop/archive.txt',
    'outtmpl': '/Users/mini/Desktop/%(title)s.%(ext)s',
    'progress_hooks': [my_hook],
    'logger': MyLogger(),
}

#convert bookmark plist to xml
output = subprocess.Popen(['plutil', '-convert', 'xml1', '-o', '/Users/mini/Desktop/SafariBookmarks.xml', '/Users/mini/Library/Safari/Bookmarks.plist'], stdout=subprocess.PIPE)
print (output.stdout.read())

#read xml into var file
file = open("/Users/mini/Desktop/SafariBookmarks.xml", "r")

for line in file:
    
    #dirty but works to find readinglist urls
    if re.search("^					<string>http", line):
        
        #prettie output
        print ('')
        print ('---------------------------------------------------------------------------------------------------------------------')
        print ('')
        print (line[13:-10])
        print ('')

        #download url
        url = line[13:-10]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print ('')

