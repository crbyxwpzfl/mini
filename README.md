```py
strg k #github spotlight
```

```py
. #vs code in browser
alt #toggle menue bar
crtl shift g #source controll
crtl shift e #explorer
```

# mini

## [ytdl](https://github.com/ytdl-org/youtube-dl)
```zsh
python3 /Users/mini/mini/pullreadlist.py #dl readinglist
```

```zsh
cd /Volumes/transfer/see
out="/Volumes/transfer/see/%(title)s.%(ext)s"
url="https://youtube.com/playlist?list=PLaHzPX64jQ189iqTEvaWmvK0l1-Dt3ssP" #dl see

/Library/Frameworks/Python.framework/Versions/3.9/bin/youtube-dl --restrict-filenames -o $out $url --no-continue --no-check-certificate --download-archive archive.txt
```

```zsh
cd /Volumes/transfer/listen
out="/Volumes/transfer/listen/%(title)s.%(ext)s"
url="https://youtube.com/playlist?list=PLaHzPX64jQ19wU2ckGEefoUlYCNvnjkv7" #dl listen

/Library/Frameworks/Python.framework/Versions/3.9/bin/youtube-dl -x --audio-format mp3 --restrict-filenames -o $out $url --no-continue --no-check-certificate --download-archive archive.txt
```

## [handbrake](https://github.com/HandBrake/HandBrake/releases)
```zsh
cd "dir/with/mkvs"
for i in *.mkv; do /Users/mini/Downloads/HandBrakeCLI -i "$i" -o "${i%.*}.mp4" ; done   #reencode all mkvs in dir
```

## [homebridge](https://github.com/homebridge/homebridge/wiki/Install-Homebridge-on-macOS)

```zsh
~/.homebridge/config.json #put config.json here
http://localhost:8581   #homebridge web ui url
```
[cmd4 plugin](https://github.com/ztalbot2000/homebridge-cmd4)<br>
[ffmpeg plgin](https://github.com/Sunoo/homebridge-camera-ffmpeg)<br>

## python
```py
python -m pip install requests    #install requests
python -m pip install --upgrade youtube-dl  #install ytdl
```

## ssh
```zsh
chmod 600 /path/to/openssh-private/   #set permissions for key file
ssh user@ip -i "path/to/openssh-private"
```

## general
```zsh
defaults write com.apple.finder AppleShowAllFiles TRUE  #show hidden files in finder
killall Finder
chflags hidden /path/to/folder #hide a folder
/Users/mini/Library/Android/sdk/emulator/emulator -list-avds #list vms
/Users/mini/Library/Android/sdk/emulator/emulator @Pixel_4_API_30 -no-window #run vm headless
/Users/mini/Library/Android/sdk/emulator/emulator @Pixel_4_API_30 -avd wa -netdelay none -netspeed full #keine ahnung mehr
rm -rf #drag drop icloud drive folders to delete them
```

## git
```zsh
git #then follow promt
git -c core.sshCommand="ssh -i /path/to/sshprivate" pull #to pull changes
```

## node
```zsh
npm cache clean -f  #node update
npm install -g n
sudo n stable
sudo npm install -g npm #update npm
npm update #update local pacages
npm update -g #update gobal packages
``` 
