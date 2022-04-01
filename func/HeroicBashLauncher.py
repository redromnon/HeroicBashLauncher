#Main file that takes bash arguments

import os,sys
import configpath
from frombash import frombash
from listinstalled import listinstalled
from steam import createscript, addtosteam
from flatpak import launchflatpakgame

#Check if Zenity is installed
print("Checking if Zenity is installed:")
checkzenity = os.system('zenity --version')

if (os.path.exists(configpath.legendaryinstalledpath) == True or os.path.exists(configpath.goginstalledpath) == True) and checkzenity == 0:

    #If len of arguments is 1 (no extra arguements), then proceed to create launch files for all games
    #   else, update parameters of a game through launch file

    if len(sys.argv) == 1: #Only name of file as default argument
    
        listinstalled()

        if "deck" in os.path.expanduser("~"):
            os.system('zenity --info --title="Process Finished" --text="Launch scripts stored in GameFiles folder\n\nYour games have been synced to Steam\n\nHave fun gaming!" --width=300')
        else:
            os.system('zenity --info --title="Process Finished" --text="Launch scripts stored in GameFiles folder\n\nYou can sync games to Steam via AddToSteam\n\nHave fun gaming!" --width=300')

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
elif checkzenity != 0:
    
    print("Zenity not installed. Please consider doing so and try again.")
else:

    os.system('zenity --error --title="Process Stopped" --text="Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again" --width=300')