#!/bin/bash

#####

#Thanks for using Heroic Bash Launcher - A simple program that allows you to launch any of your Heroic games (Epic and GOG) from literally 
#anywhere on Linux!

#Do note that this project is open-source and is under the GPL-3.0 License. For more information, you can check out the LICENSE.md file.
#Moreover, this software does not come without any warranty.

#Hope you liked my little project! Have fun gaming!

#-- Redromnon

#####

#Create log
exec > HeroicBashLauncher.log 2>&1

#Enable UTF-8 Encoding
export LC_ALL=en_US.UTF-8

#Run HeroicBashLauncher executable
chmod +x HeroicBashLauncher
./HeroicBashLauncher



