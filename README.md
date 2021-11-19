# HeroicBashLauncher

Ever wanted to launch your EGS games installed through [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) directly from the terminal, Lutris or any other frontend game launcher?
Heroic Bash Launcher lets you do exactly that. 

You can now launch your game directly without having to open Heroic at all. There's no need to run `heroic` to find the game's launch command.

![My Post](https://user-images.githubusercontent.com/74495920/142612133-f92a69d3-6a8d-451f-bd91-67e5315d11c3.png)

## Pre-requisites
- Heroic Games Launcher 1.10 'Kizaru'
- Python 3


## Working

Heroic Bash Launcher automatically detects installed games and creates a launch file for each game. The launch file is created using the *bash shell script*, i.e. `.sh` files. For example, if I have Rocket League installed, it will create the launch file titled "Sugar.sh".

Every game's launch file will contain all the launch parameters according to the game's setting in Heroic Games Launcher, including cloud syncing for supported games.

All these launch files will be available in the `GamesFiles` folder. 

You can execute a game's launch file using the terminal like `./Sugar.sh` or your preferred game launcher/manager like Lutris or EmulationStation.

**Note: For now, all launch files will be titled according to how [legendary](https://github.com/derrod/legendary) names the games (AppName.sh). You can look for your preferred game's AppName by opening Heroic Games Launcher and navigating to the bottom of the game's "Settings" window.**


## Usage

Execute the program by running `./HeroicBashLauncher.sh` in your terminal. You will be required to enable executable permissions for this file.

**Keep in mind, you have to run this program everytime you change the Settings in the Heroic Games Launcher app. This helps to overwrite the old launch parameters with the new ones.**


## Features Planned

- Name files according to the actual game name
- Ask user for a default path for saving game launch files
- Only update game launch files whose setting is changed
- Additional game launch options support (Eg. ARK)
- Automatically update launch parameters when executing game launch file

## Issues
- Uninstalled games will get detected because of leftover files. (AppName.json files in `~/.config/heroic/GamesConfig`)

## Changelog

Version 1.0 - 18/11/21


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.
