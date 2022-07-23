#Main file that takes bash arguments

import os, sys, requests, logging
from func import configpath
from func.createlaunchfile import createlaunchfile
from func.listinstalled import listinstalled
from func.steam import createscript, addtosteam
from func import settings

#Check if Zenity is installed
checkzenity = os.system('zenity --version')

#Version
curr_version = "v2.8.1"
print("Using Bash Launcher " + curr_version + "\nNOTE - This is an independent project and not affiliated with Heroic Games Launcher.\n")


if("Games/Heroic/" in os.getcwd()):
    if (os.path.exists(configpath.legendaryinstalledpath) == True or os.path.exists(configpath.goginstalledpath) == True) and checkzenity == 0:

        #If len of arguments is 1 (no extra arguements), then proceed to create launch files for all games
        #   else, update parameters of a game through launch file

        if len(sys.argv) == 1: #Only name of file as default argument
        
            #Setup logging
            logging.basicConfig(filename='HeroicBashLauncher.log', filemode='w', level=logging.DEBUG, format='[%(levelname)s] %(message)s')

            #Print current version
            logging.info("Using Bash Launcher " + curr_version + "\nNOTE - This is an independent project and not affiliated with Heroic Games Launcher.\n")
            
            #Check if a newer version is available
            new_release = False
            checkifonline = True

            #Get new version tag if there's an internet connection
            try:
                release_info = requests.get("https://api.github.com/repos/redromnon/HeroicBashLauncher/releases/latest")
                new_release_note = ("A newer version " + release_info.json()["tag_name"] + " is available!\n" +
                                    "Please visit https://github.com/redromnon/HeroicBashLauncher/releases to download the latest release.")

                if curr_version != release_info.json()["tag_name"] and not release_info.json()["prerelease"]:
                    new_release = True
                    logging.info(new_release_note)
            except:
                checkifonline = False
                logging.warning("No internet connection detected.\n\n")


            #Check if AppImage version is being used
            if(os.path.isdir(os.getcwd() + '/binaries')):
                logging.info("Detected 'binaries' folder. Making the binaries executable.")
                os.system("chmod +x binaries/legendary")
                os.system("chmod +x binaries/gogdl")

            
            if "deck" in os.path.expanduser("~"):
                os.system('zenity --info --title="Process Starting" --text="This may take a while depending on your internet connection and number of games" --width=300 --timeout=8')
            
            #Setup/Read settings file
            settings.create_settings_file()
            settings.read_settings_file()

            #Start creating scripts
            listinstalled()

            #Don't create AddToSteam script if Steam Deck 
            if "deck" in os.path.expanduser("~"):
                os.system('zenity --info --title="Process Finished" --text="Launch scripts stored in GameFiles folder\n\nYour games have been synced to Steam\n\nMake sure to launch newly installed games from Heroic first\n\nHave fun gaming!" --width=300 --timeout=8')
            else:
                os.system('zenity --info --title="Process Finished" --text="Launch scripts stored in GameFiles folder\n\nYou can choose to add the launch scripts to any game launcher and sync games to Steam via AddToSteam\n\nMake sure to launch newly installed games from Heroic first\n\nHave fun gaming!" --width=300 --timeout=8')
                logging.info("Creating AddToSteam script...")
                createscript()

            #Display new release dialog
            if new_release == True and checkifonline == True:
                os.system('zenity --info --title="Process Paused" --text="' + new_release_note + '" --width=300')
        elif len(sys.argv) == 2: #Contains simplified gamename as arg for Steam addition
            
            #Setup logging
            logging.basicConfig(filename='AddToSteam.log', filemode='w', level=logging.DEBUG, format='[%(levelname)s] %(message)s')
            
            #Read settings file
            settings.read_settings_file()
            
            logging.info("Running AddToSteam.sh...")
            
            if sys.argv[1] == "":
                    logging.info("No game selected")
                    sys.exit()
            else:
                os.system('zenity --info --title="Process Running" --text="This may take a while depending on your internet connection and number of games" --width=350')
                for i in sys.argv[1].split("|"):
                    addtosteam(i)

                os.system('zenity --info --title="Process Finished" --text="Check AddToSteam.log for details." --width=300') 
        else: #Update launch script
            createlaunchfile(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif checkzenity != 0:
        
        logging.error("Zenity not installed. Please consider doing so and try again.")
    else:

        os.system('zenity --error --title="Process Stopped" --text="Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again" --width=300')
        logging.error("Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again")
else:
    os.system('zenity --error --title="Process Stopped" --text="Please unzip or copy the HeroicBashLauncher folder to ~/Games/Heroic" --width=300')
    logging.critical("Please unzip or copy the HeroicBashLauncher folder to ~/Games/Heroic")