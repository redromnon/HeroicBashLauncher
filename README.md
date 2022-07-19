<img alt="GitHub" src="https://img.shields.io/github/license/redromnon/HeroicBashLauncher?style=for-the-badge">   <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/redromnon/HeroicBashLauncher?color=blue&include_prereleases&style=for-the-badge">    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/redromnon/HeroicBashLauncher?color=yellow&style=for-the-badge">  <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/redromnon/HeroicBashLauncher?color=blueviolet&style=for-the-badge">  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/redromnon/HeroicBashLauncher?color=green&style=for-the-badge">  <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/redromnon/HeroicBashLauncher/total?color=red&style=for-the-badge">  <a href="https://www.buymeacoffee.com/redromnon" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="28" width="130"></a>

# HeroicBashLauncher

**NOTE - This is an independent project and not affiliated with Heroic Games Launcher.**

Ever wanted to launch your [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) game library directly from the Steam or any other frontend game launcher without opening Heroic? 
Bash Launcher does exactly this and takes you straight to the game!     

![Heroic Bash Launcher](https://user-images.githubusercontent.com/74495920/142615495-a4e5e811-7ee3-41b8-ae80-d6d008820f2a.png)


## Index

- [Features](#features)
- [Pre-requisites](#pre-requisites)
- [Using Bash Launcher](#using-bash-launcher)
  - [Download](#download)
  - [Running the Program](#running-the-program)
  - [Configuring Settings](#configuring-settings)
  - [Launching Games](#launching-games)
- [Handy Guides](#handy-guides)
- [Issues and Suggestions](#issues-and-suggestions)
- [Building and Testing](#building-and-testing)
- [License](#license)
- [Support](#support)


## Features

✔️ Creates game launch scripts for installed Epic & GOG games that act as shortcuts

✔️ Includes all launch parameters including cloud save-syncing (EPIC GAMES ONLY) set in Heroic's Game Settings

✔️ Syncs games to Steam along with artwork*

✔️ Enables per game profile customization for Steam Deck users

✔️ Users can add game launch scripts to any game library or manager like Lutris, GameHub, GNOME Games, etc.


*It is recommended to use the "Add To Steam" feature in Heroic (v2.4.0+)


## Pre-requisites
- Heroic
- Zenity
- glibc v2.31+


## Using Bash Launcher

### Download
Head over to the [Releases](https://github.com/redromnon/HeroicBashLauncher/releases) page. Then download and extract the **.zip** file of the latest release.

### Running the Program
Execute the program by simply  double-clicking the HeroicBashLauncher executable. You should be greeted by the _Process Finished_ dialog at the end. Don't forget to enable executable permission - you can achieve that by doing a right-click and selecting Properties. 

### Configuring Settings

Open the `settings.config` file and disable an option by changing "true" to "false".

The following options are available:
- `"artwork"` - Downloads artwork for adding games to Steam
- `"epic"` - Creates scripts for your Epic library
- `"gog"` - Creates scripts for your GOG library

### Launching Games

#### Steam Deck users
Your games will be automatically added to Steam along with the artwork. Just open Steam or switch to the Deck UI Mode to launch your titles.

#### Desktop users
- Run your game by executing the game's launch script by double-clicking the game's launch scipt or running ```./<gamename>_Heroic.sh```
- Using your preferred game launcher/manager, just point the executable path to the game's launch script or just run `AddToSteam.sh` to add and launch games from Steam. Simple!

**Don't copy or move the game files and launch scripts anywhere else, it won't work.** 


## Handy Guides

- [Bash Launcher Wiki](https://github.com/redromnon/HeroicBashLauncher/wiki)
- [Flatpak/Steam Deck extended guide](https://github.com/redromnon/HeroicBashLauncher/wiki/Steam-Deck-(Flatpak)-Guide)
- [Adding Heroic games to Lutris and GameHub](https://github.com/redromnon/HeroicBashLauncher/wiki/Adding-Games-to-Game-Launchers-&-Managers)
- [Syncing games to Steam](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher/wiki/Adding-Games-to-Steam-on-Linux#adding-your-games-to-steam)


## Issues and Suggestions

**Do note that I don't have a Deck and this tool wasn't developed with the Steam Deck in mind, thus you may encounter Deck-specific issues.**

Before submitting an issue :

- Make sure you've run the game from Heroic atleast once

- Restart Steam after adding the launch scripts if the games don't launch. 

- Disable the Proton compatibility layer for the newly added launch script. You're not trying to run a game but a script.

- Try using Wine-GE instead of Proton, since Proton is made for Steam games in mind.

- Check if the added game's TARGET *(Right Click Game -> Properties -> SHORTCUT)* points to the correct path in Steam

If it's not working for you, consider checking the logs. The logs for the game launch scripts and the program are present in `/GameFiles/logs`and the `HeroicBashLauncher.log` respectively.

Feel free to suggest any new features and post issues in the _heroic-bash-launcher_ channel by joining [Heroic's Discord server](https://discord.gg/kXADMWbqu2). 


## Building and Testing
Since the program makes use of an executable, you will need **Python version 3.8+ and PyInstaller** to build the code.

You will also need [wget](https://pypi.org/project/wget/) and [requests](https://pypi.org/project/requests/).

To test the program, open the terminal in the `func` directory and use the following command to build -

```
 pyinstaller HeroicBashLauncher.py --onefile --strip
```

This will generate an executable stored in the `dist` folder. Copy the executable, paste it in `HeroicBashLauncher` and run it.


## License
This project is under the GNU GPLv3 license. You can take a look at LICENSE.md for more information.

Makes use of these amazing projects -
[Legendary](https://github.com/derrod/legendary),
[heroic-gogdl](https://github.com/Heroic-Games-Launcher/heroic-gogdl) and
[Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher).


## Support
Like my work!? Feel free to Buy Me A Coffee.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/redromnon)
