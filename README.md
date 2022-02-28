<img alt="GitHub" src="https://img.shields.io/github/license/redromnon/HeroicBashLauncher?style=for-the-badge">   <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/redromnon/HeroicBashLauncher?color=blue&include_prereleases&style=for-the-badge">    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/redromnon/HeroicBashLauncher?color=yellow&style=for-the-badge">  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/redromnon/HeroicBashLauncher?color=blueviolet&style=for-the-badge">  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/redromnon/HeroicBashLauncher?color=green&style=for-the-badge">

# HeroicBashLauncher

Ever wanted to launch your Epic Games Store games installed through [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) directly from the terminal, Lutris, Steam or any other frontend game launcher? 
Heroic Bash Launcher lets you do this very easily. 

You can now launch your game directly without having to open Heroic at all. There's no need to run `heroic` to find the game's launch command or write your own launch script with [Legendary](https://github.com/derrod/legendary)! Thus saving your time!


![Heroic Bash Launcher](https://user-images.githubusercontent.com/74495920/142615495-a4e5e811-7ee3-41b8-ae80-d6d008820f2a.png)


## Pre-requisites
- Heroic 2.0.0+ (AppImage in development)
- Zenity

## Building & Testing
Since the program makes use of an executable, you will need **Python version 3.8+ and PyInstaller** to build the code.

To test the program, open the terminal in the `func` directory and use the following command to build -

```
pyinstaller HeroicBashLauncher.py --onefile -p <fullpath>/HeroicBashLauncher/func
```

This will generate an executable stored in the `dist` folder. Copy the executable, paste it in the `~/HeroicBashLauncher` and run it.

## Installation
Head over to the [Releases](https://github.com/redromnon/HeroicBashLauncher/releases) page. Then download and extract the **.zip** file of the latest release.

## Usage

### Running the Program
Execute the program by simply double-clicking the **HeroicBashLancher** executable (You might need to enable executable permission). You should be greeted by the _Process Finished_ dialog at the end.

Using the Heroic Games Launcher **AppImage**? Make sure to [read this.](https://github.com/redromnon/HeroicBashLauncher/wiki/FAQ#why-are-my-games-not-launching-i-use-heroic-via-appimage)


### Running Games
You can run your game by executing the game's launch file using the terminal like ```./RocketLeague.sh```. Or using your preferred game launcher/manager, just point the executable path to the game's launch file (`~/HeroicBashLauncher/GameFiles/RocketLeague.sh`). Simple!

**Don't copy or move the game files anywhere else, it won't work.**


## Working

Heroic Bash Launcher automatically detects installed games and creates a launch file for each game. It basically reads the `.json` files stored in `~/.config/heroic/GamesConfig`. 

The launch file is created using the *bash shell script*, i.e. `.sh` files. For example, if I have Rocket League installed, it will create the launch file titled "RocketLeague.sh". All these launch files will be available in the **GameFiles** folder. 

Every game's launch file will contain all the launch parameters according to the game's setting in Heroic Games Launcher, including cloud syncing for supported games. 

Here's an *example* below of "RocketLeague.sh" -

```
#!/bin/bash 

#Game Name = Rocket League®

#App Name (Legendary) = Sugar

#Overrides launch parameters
cd .. && ./HeroicBashLauncher "Rocket League®" "Sugar" "/home/redromnon/.config/heroic/GamesConfig/Sugar.json" 



PULSE_LATENCY_MSEC=60 WINEESYNC=1 mangohud --dlsym /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --wine '/home/redromnon/.local/share/lutris/runners/wine/lutris-ge-7.1-1-x86_64/bin/wine64' --wine-prefix '/home/redromnon/.wine' || ( zenity --warning --title="Offline" --text="Cannot connect to Epic servers. Running game in offline mode." --width=200 --timeout=2 ; PULSE_LATENCY_MSEC=60 WINEESYNC=1 mangohud --dlsym /opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary launch Sugar --offline --wine '/home/redromnon/.local/share/lutris/runners/wine/lutris-ge-7.1-1-x86_64/bin/wine64' --wine-prefix '/home/redromnon/.wine' 
```


## Features Planned

- Ask user for a default path for saving game launch files
- Additional game launch options support (Eg. ARK)
- GOG Games Support
- Flatpak Support
- GUI


## Issues
If the program doesn't produce the game bash files (launch files), update the launch parameters or displays an error dialog, consider running the program from the terminal like `./HeroicBashLauncher` and post the log as an issue.


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.


## You can check out the Wiki for [FAQs](https://github.com/redromnon/HeroicBashLauncher/wiki/FAQ) and [Changelog](https://github.com/redromnon/HeroicBashLauncher/wiki/Changelog)
