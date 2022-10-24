```
strg k  #github spotlight
```

```
vscode.dev  #vs code in browser
alt  #toggle menue bar
```

### mini
```bash
defaults write com.apple.finder AppleShowAllFiles TRUE && killall Finder  #show hidden files in finder
chflags hidden /path/to/folder  #hide a folder
rm -rf #drag drop icloud drive folders to delete them then relauche finder
open /usr/local/bin/  #aria2c + ffmpeg  + ffplay  + ffprobe (yt-dlp) (code-server) binaries here
open /Users/mini/Library/Python  #python versions live here
```

### [ffmpeg](https://www.ffmpeg.org/download.html)
```
# /usr/local/bin/ffmpeg binary from webpage
ffmpeg -n -i /input.mkv (-i subs.srt or -map 0) -metadata title= -vcodec copy -acodec copy -scodec "mov_text" -ac 8 file.mp4 #when still not playable check for yuv420
```

### [vs](https://github.com/coder/code-server)
```sh
curl -fsSL https://code-server.dev/install.sh | sh -s -- --dry-run  #omit dry run to install
code-server  #and follow promts
code-server serve #serve server
code-server unregister #to fix connection bug
```

### [aria2c](https://github.com/aria2/aria2)
```sh
# /usr/local/bin/aria2c binary from gh rp
```

### [android studio](https://developer.android.com/studio)
```bash
# installed via installer
/Users/mini/Library/Android/sdk/emulator/emulator -list-avds  #list vms
/Users/mini/Library/Android/sdk/emulator/emulator -avd name -no-window  #run vm headless
/Users/mini/Library/Android/sdk/emulator/emulator -avd name -netdelay none -netspeed full  #und mehr
```

### [homebridge](https://github.com/homebridge/homebridge) + [cmd](https://github.com/ztalbot2000/homebridge-cmd4) + [cam](https://github.com/Sunoo/homebridge-camera-ffmpeg)
```sh
homebridge -D -U /path/to/config #  bring hb up in debug mode and config path
```

### [python](https://pypi.org/project/requests/) + [dlp](https://github.com/yt-dlp/yt-dlp)
```bash
python3 -m pip install requests  #install requests
python3 -m pip install --upgrade yt-dlp  #install dlp and update dlp
pip3 list  #list all installed packages
pip3 list --outdated  #smae same but just outdated
```

### ssh
```bash
chmod 600 /path/to/openpriv/   #set permissions for key file
ssh user@ip -i "path/to/openssh-private"
```

### [node](https://nodejs.org/) + [npm](https://docs.npmjs.com/)
```bash
# installed via installer
npm show node  #show newest node verison
node -v  #compare version with lts or v16lts or website
# then update either via npm install -g node@version or installer from nodejs.org
```
```bash
sudo npm cache clean -f  #clean npm cache
npm -g ls  #list ackages globally
npm -g outdated  #checkfor updates globaly
``` 

### screen
```sh
ctrl a d  # detatch from screen
ctrl a :  # enter cmd like copy for copymode
screen -list  # list current up screens
screen -r name  # connect to detacched screen
screen -S name -d -m cmd #  start named detached screen running a cmd
nano ~/.screenrc #  add or crate rc file with conent down below
```
```
# set scroll buffer
defscrollback 100000

# bind ? to scroll mode
bindkey "?" copy

# Enable mouse scrolling and scroll bar history scrolling
# termcapinfo xterm* ti@:te@
```
