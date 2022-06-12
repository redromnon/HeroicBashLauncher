<img alt="GitHub" src="https://img.shields.io/github/license/redromnon/HeroicBashLauncher?style=for-the-badge">   <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/redromnon/HeroicBashLauncher?color=blue&include_prereleases&style=for-the-badge">    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/redromnon/HeroicBashLauncher?color=yellow&style=for-the-badge">  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/redromnon/HeroicBashLauncher?color=blueviolet&style=for-the-badge">  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/redromnon/HeroicBashLauncher?color=green&style=for-the-badge">  <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/redromnon/HeroicBashLauncher/total?color=red&style=for-the-badge">

# HeroicBashLauncher

**NOTE - This is an independent project and not affiliated with Heroic Games Launcher.**

Ever wanted to launch your [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) game library directly from the Steam, Lutris, GameHub or any other frontend game launcher? 
Bash Launcher does exactly this and takes you straight to the game!     

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
- [Support](#support)


## Features

✔️ Creates launch scripts for installed Epic & GOG games that act as shortcuts

✔️ Includes all launch parameters including cloud save-syncing set in Heroic's Game Settings

✔️ Displays a GUI list to add games (add the launch scripts and download artwork) to Steam for Linux Desktop users

✔️ Automatically syncs games (adds the launch scripts and download artwork) to Steam for Steam-Deck users


## Pre-requisites
- Heroic 2.2.2+
- Zenity
- glibc v2.31+


## Using Bash Launcher

### Download
Head over to the [Releases](https://github.com/redromnon/HeroicBashLauncher/releases) page. Then download and extract the **.zip** file of the latest release.

### Running the Program
Execute the program by simply  double-clicking the `setup.sh` script. You should be greeted by the _Process Finished_ dialog at the end.

### Launching Games

#### Steam Deck users
Your games will be automatically added to Steam along with the artwork. Just open Steam or switch to the Deck UI Mode to launch your titles.

#### Desktop users
- Run your game by executing the game's launch script by double-clicking the game's launch scipt or running ```./<gamename>_Heroic.sh```
- Using your preferred game launcher/manager, just point the executable path to the game's launch script or just run `AddToSteam.sh` to launch games from Steam. Simple!

**Don't copy or move the game files and launch scripts anywhere else, it won't work.** 


## Handy Guides

- [Bash Launcher Wiki](https://github.com/redromnon/HeroicBashLauncher/wiki)
- [Flatpak/Steam Deck extended guide](https://github.com/redromnon/HeroicBashLauncher/wiki/Steam-Deck-(Flatpak)-Guide)
- [Adding Heroic games to Lutris and GameHub](https://github.com/redromnon/HeroicBashLauncher/wiki/Adding-Games-to-Game-Launchers-&-Managers)
- [Syncing games to Steam](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/wiki/Adding-Games-to-Steam-on-Linux#adding-your-games-to-steam)


## Issues and Suggestions

**Do note that I don't have a Deck, so you may encounter Deck-specific issues.**

Before submitting an issue :

- Make sure you've run the game from Heroic atleast once

- Restart Steam after adding the launch scripts if the games don't launch. 

- Disable the Proton compatibility layer for the newly added launch script. You're not trying to run a game but a script.

- Try using Wine-GE instead of Proton, since Proton is made for Steam games in mind.

If it's not working for you, consider checking the logs. The logs for the game launch scripts and the program are present in `/GameFiles/logs`and the base directory respectively.

Feel free to suggest any new features and post issues in the _heroic-bash-launcher_ channel by joining [Heroic's Discord server](https://discord.gg/kXADMWbqu2). 


## Building and Testing
Since the program makes use of an executable, you will need **Python version 3.8+ and PyInstaller** to build the code.

You will also need [wget (for Python)](https://pypi.org/project/wget/).

To test the program, open the terminal in the `func` directory and use the following command to build -

```
 pyinstaller HeroicBashLauncher.py --onefile --strip
```

This will generate an executable stored in the `dist` folder. Copy the executable, paste it in `HeroicBashLauncher` and run it.


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.

Makes use of the following projects -
[Legendary](https://github.com/derrod/legendary),
[heroic-gogdl](https://github.com/Heroic-Games-Launcher/heroic-gogdl) and
[Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher).


## Support
If you like my work and wish to support it, feel free to Buy Me A Coffee.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/redromnon)
