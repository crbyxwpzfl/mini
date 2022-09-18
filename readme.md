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

### [ffmpeg](https://www.ffmpeg.org/download.html)

### [dlp](https://github.com/yt-dlp/yt-dlp)

### [aria2c](https://github.com/aria2/aria2)

### python
```bash
python3 -m pip install requests    #install requests
python3 -m pip install -U yt-dlp   #install dlp
```

### ssh
```bash
chmod 600 /path/to/openssh-private/   #set permissions for key file
ssh user@ip -i "path/to/openssh-private"
```

### general
```bash
defaults write com.apple.finder AppleShowAllFiles TRUE && killall Finder  #show hidden files in finder
chflags hidden /path/to/folder  #hide a folder
rm -rf #drag drop icloud drive folders to delete them
```

### [android studio](https://developer.android.com/studio)
```bash
/Users/mini/Library/Android/sdk/emulator/emulator -list-avds                                             #list vms
/Users/mini/Library/Android/sdk/emulator/emulator @Pixel_4_API_30 -no-window                             #run vm headless
/Users/mini/Library/Android/sdk/emulator/emulator @Pixel_4_API_30 -avd wa -netdelay none -netspeed full  #und mehr
```

### git
```bash
git #then follow promt
git -c core.sshCommand="ssh -i /path/to/sshprivate" pull #to pull changes
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
