from __future__ import unicode_literals
import sys
import re
import subprocess

#import ytdl via path
sys.path.append("/usr/local/bin/youtube-dl")
import youtube_dl

def my_hook(d):
    if d['status'] == 'finished':
        print(d['filename'])

#set ytdl options
ydl_opts = {
    'simulate': False,
    'restrict-filenames': False,
    'ignoreerrors': True,
    'download_archive': '/Users/mini/Desktop/archive.txt',
    'outtmpl': '/Users/mini/Desktop/%(title)s.%(ext)s',
    'progress_hooks': [my_hook],
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