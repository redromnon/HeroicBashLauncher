#Main file that takes bash arguments

import os,sys
from frombash import frombash
from listinstalled import listinstalled

#Take arguments
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]

if os.path.exists(os.path.expanduser("~") + "/.config/legendary/installed.json") == True:

    #If arg1 is "", then proceed to create launch files for all games
    #   else, update paramters of a game
    if arg1 == "":
    
        listinstalled()
        os.system('zenity --info --title="Process Finished" --text="Launch files stored in GameFiles folder.\n\nHave fun gaming!" --width=200')
    else:
        frombash(arg1, arg2, arg3)
else:

    os.system('zenity --error --title="Process Stopped" --text="Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again." --width=200')