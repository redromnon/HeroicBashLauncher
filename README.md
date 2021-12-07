# HeroicBashLauncher

Ever wanted to launch your Epic Games Store games installed through [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) directly from the terminal, Lutris, Steam or any other frontend game launcher? 
Heroic Bash Launcher lets you do this very easily. 

You can now launch your game directly without having to open Heroic at all. There's no need to run `heroic` to find the game's launch command or write your own launch script with [Legendary](https://github.com/derrod/legendary)! Thus saving your time!


![Heroic Bash Launcher](https://user-images.githubusercontent.com/74495920/142615495-a4e5e811-7ee3-41b8-ae80-d6d008820f2a.png)


## Pre-requisites
- Heroic Games Launcher 1.10 'Kizaru'
- Python 3
- Git


## Working

Heroic Bash Launcher automatically detects installed games and creates a launch file for each game. The launch file is created using the *bash shell script*, i.e. `.sh` files. For example, if I have Rocket League installed, it will create the launch file titled "Sugar.sh".


All these launch files will be available in the **GameFiles** folder. 


**For now, all launch files will be titled according to how legendary names the games (AppName.sh). The game's actual name will be mentioned in the launch file, as seen below.**

Every game's launch file will contain all the launch parameters according to the game's setting in Heroic Games Launcher, including cloud syncing for supported games. Here's an example below of "Sugar.sh" -

```
#!/bin/bash

#Game Name = Rocket League®

cd .. && ./HeroicBashLauncher.sh #Overrides launch parameters

PULSE_LATENCY_MSEC=60 WINE_FULLSCREEN_FSR=1 WINE_FULLSCREEN_FSR_STRENGTH=1 WINEESYNC=1 MANGOHUD=1 /usr/bin/gamemoderun /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --wine '/home/redromnon/.local/share/lutris/runners/wine/lutris-ge-6.21-1-x86_64/bin/wine64' --wine-prefix '/home/redromnon/.wine' || (echo "NO INTERNET CONNECTION. Running game in offline mode..." && PULSE_LATENCY_MSEC=60 WINE_FULLSCREEN_FSR=1 WINE_FULLSCREEN_FSR_STRENGTH=1 WINEESYNC=1 MANGOHUD=1 /usr/bin/gamemoderun /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --offline --wine '/home/redromnon/.local/share/lutris/runners/wine/lutris-ge-6.21-1-x86_64/bin/wine64' --wine-prefix '/home/redromnon/.wine' )
```


## Installation
Run the following commands in your terminal -
```
git clone https://github.com/redromnon/HeroicBashLauncher.git
cd HeroicBashLancher
```

## Usage

### Running the Program
Execute the program by running the following command `./HeroicBashLauncher.sh` or simply double-click this file. 
You will be required to enable executable permissions for this file.


### Running Games
You can run your game by executing the game's launch file using the terminal like ```./Sugar.sh```. Or using your preferred game launcher/manager, just point the executable path to the game's launch file. Simple!


### Updating the Program
Use `git pull` to get the latest changes.


## Features Planned

- Ask user for a default path for saving game launch files
- Only update game launch files whose setting is changed
- Additional game launch options support (Eg. ARK)


## Issues
Feel free to report any!


## Changelog

- Version 1.4 - 7/12/21

  - *Launch parameters auto-update when running any game's launch file. 
  (**Note** - As of versions 1.3 and below, you had to run the program everytime you changed launch parameters in the Heroic app. Now, you DON'T need to do this.)*

- Version 1.3 - 5/12/21

  - *Fixed bug that launched two instances of a game*

- Version 1.2 - 25/11/21

  - *Games now run in offline mode if no internet connection is detected.* 
  - *The save path is also included in the cloud save-sync parameter.* 

- Version 1.1 - 20/11/21

  - *Launch files of uninstalled games won't be generated due to left over files.* 
  - *The game's actual name will be displayed and mentioned in the bash script.*

- Version 1.0.1 - 18/11/21

  - *Now detects if no games are installed and displays a relevant message.*  

- Version 1.0 - 18/11/21


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.
