from __future__ import unicode_literals
import sys
import re
import subprocess

sys.path.append("/usr/local/bin/youtube-dl")
import youtube_dl

ydl_opts = {
    'simulate': True,
    'restrict-filenames': True,
    'ignoreerrors': True,
    'download_archive': '/Users/mini/Desktop/archive.txt',
    'outtmpl': '/Users/mini/Desktop/%(title)s.%(ext)s',
}


output = subprocess.Popen(['plutil', '-convert', 'xml1', '-o', '~/Desktop/SafariBookmarks.xml', '~/Library/Safari/Bookmarks.plist'], stdout=subprocess.PIPE)

file = open("/Users/mini/Desktop/SafariBookmarks.xml", "r")

for line in file:
    if re.search("^					<string>http", line):
        print ('')
        print (line[13:-10]'------------------------------------------------------------------------------')
        print ('')
        url = line[13:-10]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
