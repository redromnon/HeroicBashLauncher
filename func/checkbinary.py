#TO USE LEGENDARY OR GOGDL
#   For AppImage, check if alternavtive binary (Legendary) is added.
#   If not, check folder under /tmp/ that includes path to the binaries.

import os, json, sys, traceback
from func import configpath

def getbinary(gametype):

    try:

        #Path to heroic's configuration json file
        #heroicconfigpath = os.path.expanduser("~") + "/.config/heroic/config.json"

        #Convert config json to dict
        with open(configpath.heroicconfigpath, encoding='utf-8') as p:
            heroicconfig = json.load(p)

        #Checking
        binary = ""

        if os.path.exists("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux") == True:

            if gametype != "epic":
                binary = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/gogdl "
            else:
                binary = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary "
        elif 'altLegendaryBin' in heroicconfig['defaultSettings'].keys() and heroicconfig["defaultSettings"]["altLegendaryBin"] != "" and gametype == "epic":

                binary = heroicconfig["defaultSettings"]["altLegendaryBin"] + " "
        #elif 'altGogdlBin' in heroicconfig['defaultSettings'].keys() and heroicconfig["defaultSettings"]["altGogdlBin"] != "" and gametype != "epic":
        
                #binary = heroicconfig["defaultSettings"]["altGogdlBin"] + " "
        elif os.path.exists("/var/lib/flatpak/app/com.heroicgameslauncher.hgl") or os.path.exists("/app/bin/heroic"):#System or Flatpak-env path

            if gametype != "epic":
                binary = "/app/bin/heroic/resources/app.asar.unpacked/build/bin/linux/gogdl "
            else:
                binary = "/app/bin/heroic/resources/app.asar.unpacked/build/bin/linux/legendary "
        else:#AppImage

            if gametype != "epic":
                binary = os.getcwd() + "/binaries/gogdl "
            else:
                binary = os.getcwd() + "/binaries/legendary "
            
        return binary
    except Exception:

        print(traceback.format_exc())
        os.system('zenity --error --title="Process Failed" --text="\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
        sys.exit()