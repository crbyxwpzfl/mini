# mini

## python
```bash
python -m pip install requests    #install requests
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