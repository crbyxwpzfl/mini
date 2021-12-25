from __future__ import unicode_literals
import sys

sys.path.append("/usr/local/bin/youtube-dl")

import youtube_dl


ydl_opts = {
    'restrict-filenames': True,
    'download_archive': '/Users/mini/Desktop/archive.txt',
    'outtmpl': '/Users/mini/Desktop/%(title)s.%(ext)s',
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])



import re
import sys
import subprocess

output = subprocess.Popen(['plutil', '-convert', 'xml1', '-o', '~/Desktop/SafariBookmarks.xml', '~/Library/Safari/Bookmarks.plist'], stdout=subprocess.PIPE)


#os.system('plutil -convert xml1 -o ~/Desktop/SafariBookmarks.xml ~/Library/Safari/Bookmarks.plist')



file = open("/Users/mini/Desktop/SafariBookmarks.xml", "r")

for line in file:
	if re.search("^					<string>http", line):
		print (line[13:-10])
		url = line[13:-10]
		ytdlpath = "/Library/Frameworks/Python.framework/Versions/3.9/bin/youtube-dl"
		output = subprocess.Popen([ytdlpath, '--restrict-filenames', '-o', '/Users/mini/Desktop/%(title)s.%(ext)s', url, '--no-continue', '--no-check-certificate', '--download-archive', 'archive.txt'], stdout=subprocess.PIPE)