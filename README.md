```
. #to vs code in browser
alt #to toggle menue bar
crtl shit g #to source controll
```

# mini

## [ytdl](https://github.com/ytdl-org/youtube-dl)
```
cd /Volumes/transfer/see
out="/Volumes/transfer/see/%(title)s.%(ext)s"
url="https://youtube.com/playlist?list=PLaHzPX64jQ189iqTEvaWmvK0l1-Dt3ssP" #see

/Library/Frameworks/Python.framework/Versions/3.9/bin/youtube-dl --restrict-filenames -o $out $url --no-continue --no-check-certificate --download-archive archive.txt
```

```
cd /Volumes/transfer/listen
out="/Volumes/transfer/listen/%(title)s.%(ext)s"
url="https://youtube.com/playlist?list=PLaHzPX64jQ19wU2ckGEefoUlYCNvnjkv7" #listen

/Library/Frameworks/Python.framework/Versions/3.9/bin/youtube-dl -x --audio-format mp3 --restrict-filenames -o $out $url --no-continue --no-check-certificate --download-archive archive.txt
```

## [handbrake](https://github.com/HandBrake/HandBrake/releases)
```
cd "dir/with/mkvs"
for i in *.mkv; do /Users/mini/Downloads/HandBrakeCLI -i "$i" -o "${i%.*}.mp4" ; done   #reencode all mkvs in dir
```

## python
```bash
python -m pip install requests    #install requests
sudo -H pip install --upgrade youtube-dl  #install ytdl
```

## ssh
```bash
chmod 600 /path/to/openssh-private/   #set permissions for key file
ssh user@ip -i "path/to/openssh-private"
```

## general
```bash
defaults write com.apple.finder AppleShowAllFiles TRUE  #show hidden files in finder
killall Finder
chflags hidden /path/to/folder #hide a folder
/Users/mini/Library/Android/sdk/emulator/emulator -list-avds #list vms
/Users/mini/Library/Android/sdk/emulator/emulator @Pixel_4_API_30 -no-window #run vm headless
/Users/mini/Library/Android/sdk/emulator/emulator @Pixel_4_API_30 -avd wa -netdelay none -netspeed full #keine ahnung mehr
```

## git
```
git #then follow promt
```

## node
```bash
npm cache clean -f  #node update
npm install -g n
sudo n stable
sudo npm install -g npm #update npm
npm update #update local pacages
npm update -g #update gobal packages
``` 
