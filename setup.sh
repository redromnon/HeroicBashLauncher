#!/usr/bin/bash

#####

#Thanks for using Heroic Bash Launcher - A simple program that allows you to launch any of your Heroic games (Epic and GOG) from literally 
#anywhere on Linux!

#Do note that this project is open-source and is under the GPL-3.0 License. For more information, you can check out the LICENSE.md file.
#Moreover, this software does not come with any warranty.

#Hope you liked my little project! Have fun gaming!

#-- Redromnon

#####

# Redirect all stderr/out to our logfile
exec > HeroicBashLauncher.log 2>&1

#Run HeroicBashLauncher executable
EXE=HeroicBashLauncher
# Use zenity popups when run from this script
# create launch scripts for all installed Heroic games
ARGS="--zenity --create_all"
if [ -f "$EXE" ]; then
    echo "Using $EXE Base/AppImage version..." ;
    ./${EXE} ${ARGS}
else
    echo "Using $EXE Flatpak version..." ;
    (cd GameFiles && ./${EXE} ${ARGS})
fi



