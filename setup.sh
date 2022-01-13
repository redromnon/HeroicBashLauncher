#!/usr/bin/bash

###################

#VERSION 1.6.1

#Thanks for using Heroic Bash Launcher - A simple program that allows you to launch any of your Epic Store games from literally anywhere on Linux!

#Do note that this project is open-source and is under the GPL-3.0 License. For more information, you can check out the LICENSE.md file.
#Moreover, this software does not come without any warranty.

#Hope you liked my little project! Have fun gaming!

#-- By Redromnon

###################

#Check if Zenity is installed
(echo "Checking if Zenity is installed..." ; zenity --version) || (echo "Zenity not installed, now installing it." ; sudo apt install zenity -y)

#Run the Heroic Bash Launcher program
python3 HeroicBashLauncher.py
zenity --info --title="Process finished" --text="Launch files stored in GameFiles folder.\n\nHave fun gaming!" --width=200 --timeout=3