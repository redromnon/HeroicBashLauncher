# HeroicBashLauncher

Every wanted to launch your EGS games installed through [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher) directly from the terminal, Lutris or any other frontend game launcher?
Heroic Bash Launcher lets you do exactly that. 

If you want to know the launch commands of a game, you need to run `heroic` from the terminal. Instead, you can now launch your game directly without having to open Heroic at all.


## Pre-requisites
- Heroic Games Launcher 1.10 'Kizaru'
- Python 3


## Working

Heroic Bash Launcher automatically detects installed games and creates a launch file for each game depending on the launch properties you set on Heroic Games Launcher. The launch file is created using the *bash shell script*, i.e. `.sh` files. For example, if I have Rocket League installed, it will create the launch file titled "Sugar.sh".

As mentioned earlier, every game's launch file will contain all the launch parameters according to the game's setting in Heroic Games Launcher, including cloud syncing for supported games.

All these launch files will be available in the `GamesFiles` folder. You can execute the game's launch file using the terminal like `./Sugar.sh` or your preferred game launcher/manager like Lutris or EmulationStation.

**Note: For now, all launch files will be titled according to how [legendary](https://github.com/derrod/legendary) names the games (AppName.sh). You can look for your preferred game's AppName by opening Heroic Games Launcher and navigating to the bottom of the game's "Settings" window.**


## Usage

Open your terminal and execute the program by running `./HeroicBashLauncher.sh`. You may be required to enable executable permissions for this file.

**Keep in mind, you have to run this program everytime you change the Settings in the Heroic Games Launcher app. This helps to overwrite the old launch parameters with the new ones.**


## Features Planned

- Name files according to the actual game name
- Ask user for a default path for saving game launch files
- Only update game launch files whose setting is changed
- Additional game launch options support (Eg. ARK)

## Changelog

Version 1.0 - 18/11/21


## License
This project is under the GNU GPLv3 license. You can take a look at the LICENSE.md for more information.
