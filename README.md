<img alt="GitHub" src="https://img.shields.io/github/license/redromnon/HeroicBashLauncher?style=for-the-badge">   <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/redromnon/HeroicBashLauncher?color=blue&include_prereleases&style=for-the-badge">    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/redromnon/HeroicBashLauncher?color=yellow&style=for-the-badge">  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/redromnon/HeroicBashLauncher?color=blueviolet&style=for-the-badge">  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/redromnon/HeroicBashLauncher?color=green&style=for-the-badge">  <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/redromnon/HeroicBashLauncher/total?color=red&style=for-the-badge">

# HeroicBashLauncher
Ever wanted to launch your [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) game library directly from the Steam, Lutris, GameHub or any other frontend game launcher? 
Bash Launcher does exactly this and takes to straight to the game!  

Thus, you can now stay on your launcher interface comfortably without having the need to open Heroic to launch your games at all.   

![Heroic Bash Launcher](https://user-images.githubusercontent.com/74495920/142615495-a4e5e811-7ee3-41b8-ae80-d6d008820f2a.png)


## Index

- [Features](#features)
- [Pre-requisites](#pre-requisites)
- [Using Bash Launcher](#using-bash-launcher)
  - [Download](#download)
  - [Running the Program](#running-the-program)
  - [Launching Games](#launching-games)
- [Handy Guides](#handy-guides)
- [Issues and Suggestions](#issues-and-suggestions)
- [Building and Testing](#building-and-testing)
- [License](#license)


## Features

✔️ Creates launch scipts for installed Epic & GOG games 

✔️ Includes all launch parameters set in Heroic's Game Settings

✔️ Displays a GUI list to add games (add the launch scripts) to Steam for Non-Deck users

✔️ Automatically syncs games (adds the launch scripts) to Steam for Deck users

✔️ Downloads relevant artwork


## Pre-requisites
- Heroic 2.2.2+
- Zenity


## Using Bash Launcher

### Download
Head over to the [Releases](https://github.com/redromnon/HeroicBashLauncher/releases) page. Then download and extract the **.zip** file of the latest release.

### Running the Program
Execute the program by simply running the `setup.sh` script. You should be greeted by the _Process Finished_ dialog at the end.

### Launching Games

#### Steam Deck users
Your games will be automatically added to Steam. Just open Steam or switch to the Deck UI Mode to launch your titles.

#### Non-Deck users
- Run your game by executing the game's launch script by double-clicking the game's launch scipt, using the terminal like ```./RocketLeague_Heroic.sh```
- Using your preferred game launcher/manager, just point the executable path to the game's launch script. Simple!

**Don't copy or move the game files and launch scripts anywhere else, it won't work.** 


## Handy Guides

- [Bash Launcher Wiki](https://github.com/redromnon/HeroicBashLauncher/wiki)
- [Steam Deck extended guide](https://github.com/redromnon/HeroicBashLauncher/wiki/Steam-Deck-(Flatpak)-Guide)
- [Adding Heroic games to Lutris and GameHub](https://github.com/redromnon/HeroicBashLauncher/wiki/Adding-Games-to-Game-Launchers-&-Managers)
- [Syncing games to Steam](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/wiki/Adding-Games-to-Steam-on-Linux#adding-your-games-to-steam)


## Issues and Suggestions
Before submitting an issue :

- Make sure the game launches from Heroic Games Launcher.

- You might have to restart Steam after adding the launch scripts if the games don't launch. 

- Make sure that the shorcuts.vdf file is present in `/.steam/steam/userdata/<Your-Steam-ID>/config/` (Multiple account support coming soon)

- Consider deleting any special characters from any game-related folder names (like Wine Prefix).

- Disable the Proton compatibility layer for the newly added launch script. You're not trying to run a game but a script.

If it's not working for you, consider checking the logs. The logs for the game launch scripts and the program are present in `/GameFiles/logs`and the base directory respectively.

Feel free to suggest any new features, especially those already implemented in Heroic. 


## Building and Testing
Since the program makes use of an executable, you will need **Python version 3.8+ and PyInstaller** to build the code.

You will also need [wget (for Python)](https://pypi.org/project/wget/).

To test the program, open the terminal in the `func` directory and use the following command to build -

```
pyinstaller HeroicBashLauncher.py --onefile -p <fullpath>/HeroicBashLauncher/func
```

This will generate an executable stored in the `dist` folder. Copy the executable, paste it in `HeroicBashLauncher` and run it.


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.
