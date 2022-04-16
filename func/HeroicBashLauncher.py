#!/bin/env python3
#Main file that takes bash arguments

import os,sys
import configpath
from frombash import frombash
from listinstalled import listinstalled
from steam import createscript, addtosteam
from flatpak import launchflatpakgame
from zenity import zenity_popup

#Print current version
print("Using Bash Launcher 2.4.2\n")

if (os.path.exists(configpath.legendaryinstalledpath) == True or os.path.exists(configpath.goginstalledpath) == True):

    #If len of arguments is 1 (no extra arguements), then proceed to create launch files for all games
    #   else, update parameters of a game through launch file

    if len(sys.argv) == 1: #Only name of file as default argument
    
        listinstalled()

        #Don't create AddToSteam script if Steam Deck 
        if "deck" in os.path.expanduser("~"):
            zenity_popup(title="Process Finished", text="Launch scripts stored in GameFiles folder\n\nYour games have been synced to Steam\n\nHave fun gaming!")
        else:
            zenity_popup(title="Process Finished", text="Launch scripts stored in GameFiles folder\n\nYou can sync games to Steam via AddToSteam\n\nHave fun gaming!")
            print("\nCreating AddToSteam script...")
            createscript()
    elif len(sys.argv) == 2: #Contains simplified gamename as arg for Steam addition
        
        if sys.argv[1] == "":
                print("No game selected")
                sys.exit()
        else:
            addtosteam(sys.argv[1])
    elif len(sys.argv) == 5:
        
        frombash(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        launchflatpakgame(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
else:
    zenity_popup(type=error, title="Process Stopped", text="Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again")

