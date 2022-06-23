#Main file that takes bash arguments

import os,sys, requests
from func import configpath
from func.createlaunchfile import createlaunchfile
from func.listinstalled import listinstalled
from func.steam import createscript, addtosteam

#Print current version
curr_version = "v2.7.4"
print("Using Bash Launcher " + curr_version + "\nNOTE - This is an independent project and not affiliated with Heroic Games Launcher.\n")

#Check if a newer version is available
new_release = False
checkifonline = True

#Get new version tag if there's an internet connection
try:
    release_info = requests.get("https://api.github.com/repos/redromnon/HeroicBashLauncher/releases/latest")
    new_release_note = ("A newer version " + release_info.json()["tag_name"] + " is available!\n" +
                        "Please visit https://github.com/redromnon/HeroicBashLauncher/releases to download the latest release.")

    if curr_version != release_info.json()["tag_name"]:
        new_release = True
        print(new_release_note)
except:
    checkifonline = False
    print("No internet connection detected.\n\n")


#Check if Zenity is installed
print("\nChecking if Zenity is installed...")
checkzenity = os.system('zenity --version')

if (os.path.exists(configpath.legendaryinstalledpath) == True or os.path.exists(configpath.goginstalledpath) == True) and checkzenity == 0:

    #If len of arguments is 1 (no extra arguements), then proceed to create launch files for all games
    #   else, update parameters of a game through launch file

    if len(sys.argv) == 1: #Only name of file as default argument
    
        if "deck" in os.path.expanduser("~"):
            os.system('zenity --info --title="Process Starting" --text="This may take a while depending on your internet connection and number of games" --width=300 --timeout=8')
        
        listinstalled()

        #Don't create AddToSteam script if Steam Deck 
        if "deck" in os.path.expanduser("~"):
            os.system('zenity --info --title="Process Finished" --text="Launch scripts stored in GameFiles folder\n\nYour games have been synced to Steam\n\nMake sure to launch newly installed games from Heroic first\n\nHave fun gaming!" --width=300 --timeout=8')
        else:
            os.system('zenity --info --title="Process Finished" --text="Launch scripts stored in GameFiles folder\n\nYou can choose to add the launch scripts to any game launcher and sync games to Steam via AddToSteam\n\nMake sure to launch newly installed games from Heroic first\n\nHave fun gaming!" --width=300 --timeout=8')
            print("\nCreating AddToSteam script...")
            createscript()

        #Display new release dialog
        if new_release == True and checkifonline == True:
            os.system('zenity --info --title="Process Paused" --text="' + new_release_note + '" --width=300')
    elif len(sys.argv) == 2: #Contains simplified gamename as arg for Steam addition
        
        if sys.argv[1] == "":
                print("No game selected")
                sys.exit()
        else:
            os.system('zenity --info --title="Process Running" --text="This may take a while depending on your internet connection and number of games" --width=350')
            for i in sys.argv[1].split("|"):
                addtosteam(i)

            os.system('zenity --info --title="Process Finished" --text="Check AddToSteam.log for details." --width=300') 
    else: #Update launch script
        createlaunchfile(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
elif checkzenity != 0:
    
    print("Zenity not installed. Please consider doing so and try again.")
else:

    os.system('zenity --error --title="Process Stopped" --text="Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again" --width=300')
    print("Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again")