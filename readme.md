```
strg k #github spotlight
```

```
. #vs code in browser
alt #toggle menue bar
crtl shit g #source controll
crtl shift e #explorer
```

### mini
```bash
defaults write com.apple.finder AppleShowAllFiles TRUE && killall Finder  #show hidden files in finder
chflags hidden /path/to/folder  #hide a folder
rm -rf #drag drop icloud drive folders to delete them
open /usr/local/bin/  #aria2c + ffmpeg  + ffplay  + ffprobe (yt-dlp) binaries here
open /Users/mini/Library/Python  #python versions live here
```

### [ffmpeg](https://www.ffmpeg.org/download.html)

### [aria2c](https://github.com/aria2/aria2)

### [android studio](https://developer.android.com/studio)
```bash
/Users/mini/Library/Android/sdk/emulator/emulator -list-avds  #list vms
/Users/mini/Library/Android/sdk/emulator/emulator -avd name -no-window  #run vm headless
/Users/mini/Library/Android/sdk/emulator/emulator -avd name -netdelay none -netspeed full  #und mehr
```

### [homebridge](https://github.com/homebridge/homebridge) + [cmd](https://github.com/ztalbot2000/homebridge-cmd4) + [cam](https://github.com/Sunoo/homebridge-camera-ffmpeg)
```sh
homebridge -D -U /path/to/config #  bring hb up in debug mode and config path
sudo hb-service update-node  #  helper to update node
```

### python + [dlp](https://github.com/yt-dlp/yt-dlp)
```bash
python3 -m pip install requests    #install requests
python3 -m pip install -U yt-dlp   #install dlp
```

### ssh
```bash
chmod 600 /path/to/openssh-private/   #set permissions for key file
ssh user@ip -i "path/to/openssh-private"
```

### git
```bash
git #then follow promt
git -c core.sshCommand="ssh -i /path/to/sshprivate" pull #to pull changes
sudo chmod 600 /path/to/priv #for warning file to open 
```

### node
```bash
npm cache clean -f  #node update
npm install -g n
sudo n stable
sudo npm install -g npm #update npm
npm update #update local pacages
npm update -g #update gobal packages
``` 

### screen
```sh
ctrl a d # detatch from screen
screen -list #  list current up screens
screen -r name, nr #  connect to screen
screen -S name -d -m cmd #  start named detached screen running a cmd
nano ~/.screenrc #  add or crate rc file with conent down below
```
```
# Enable mouse scrolling and scroll bar history scrolling
termcapinfo xterm* ti@:te@

```
