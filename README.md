# HeroicBashLauncher

Ever wanted to launch your EGS games installed through [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) directly from the terminal, Lutris or any other frontend game launcher?
Heroic Bash Launcher lets you do exactly that. 

You can now launch your game directly without having to open Heroic at all. There's no need to run `heroic` to find the game's launch command.


![Heroic Bash Launcher](https://user-images.githubusercontent.com/74495920/142615495-a4e5e811-7ee3-41b8-ae80-d6d008820f2a.png)


## Pre-requisites
- Heroic Games Launcher 1.10 'Kizaru'
- Python 3
- Git (Optional)


## Working

Heroic Bash Launcher automatically detects installed games and creates a launch file for each game. The launch file is created using the *bash shell script*, i.e. `.sh` files. For example, if I have Rocket League installed, it will create the launch file titled "Sugar.sh".

Every game's launch file will contain all the launch parameters according to the game's setting in Heroic Games Launcher, including cloud syncing for supported games. Here's an example below of "Sugar.sh" -

```
#!/bin/bash

#Game Name = Rocket League®



PULSE_LATENCY_MSEC=60 WINE_FULLSCREEN_FSR=1 WINE_FULLSCREEN_FSR_STRENGTH=2 WINEESYNC=1 STEAM_COMPAT_CLIENT_INSTALL_PATH=/home/redromnon/.steam/steam STEAM_COMPAT_DATA_PATH='/home/redromnon/.wine' MANGOHUD=1 /usr/bin/gamemoderun /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --no wine --wrapper "'/home/redromnon/.steam/root/compatibilitytools.d/Proton-6.21-GE-2/proton' run"
```

All these launch files will be available in the **GameFiles** folder. 

**For now, all launch files will be titled according to how [legendary](https://github.com/derrod/legendary) names the games (AppName.sh). The game's actual name will be mentioned in the launch file, as seen in the above eg.**


## Usage

First, download and extract the project folder by clicking on the green button "Code" and hit "Download Zip". Or use Git to clone.

Using your terminal, navigate to this directory and execute the program by running the following command
```./HeroicBashLauncher.sh``` 
You will be required to enable executable permissions for this file.

**Keep in mind, you have to run this program everytime you change the Settings in the Heroic Games Launcher app. This helps to overwrite the old launch parameters with the new ones.**

You can execute a game's launch file using the terminal like ```./Sugar.sh``` or your preferred game launcher/manager like Lutris or EmulationStation.


## Features Planned

- Name files according to the actual game name
- Ask user for a default path for saving game launch files
- Only update game launch files whose setting is changed
- Additional game launch options support (Eg. ARK)
- Automatically update launch parameters when executing game launch file


## Changelog

- Version 1.0 - 18/11/21
- Version 1.1 - 20/11/21


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.
