#TO USE LEGENDARY OR GOGDL
#   For AppImage, check if alternavtive binary (Legendary) is added.
#   If not, check folder under /tmp/ that includes path to the binaries.

import json, logging, os, shutil, sys, traceback
from func import configpath
from func.settings import args

resources_bin_path = "resources/app.asar.unpacked/build/bin/linux"

def getbinary(gametype):

    try:

        #Path to heroic's configuration json file
        #heroicconfigpath = os.path.expanduser("~") + "/.config/heroic/config.json"

        #Convert config json to dict
        with open(configpath.heroicconfigpath, encoding='utf-8') as p:
            heroicconfig = json.load(p)

        #Checking
        binary = ""
        
        if gametype != "epic":
            executable = "gogdl"
        else:
            executable = "legendary"

        heroic_base_path = None

        # Attempt to find heroic on path
        detected_heroic_path = shutil.which('heroic')
        if detected_heroic_path:
            # Follow any symlinks to the real path of heroic
            detected_heroic_path = os.path.realpath(detected_heroic_path)
            if os.path.exists(detected_heroic_path):
                heroic_base_path = os.path.dirname(detected_heroic_path)
        elif os.path.exists("/opt/Heroic"): # Default to /opt/Heroic
            heroic_base_path = "/opt/Heroic"
        elif configpath.is_flatpak or os.path.exists("/app/bin/heroic"): #System or Flatpak-env path
            heroic_base_path = "/app/bin/heroic"
        
        if heroic_base_path:

            heroic_resources_path = os.path.join(heroic_base_path, resources_bin_path)

            binary = os.path.join(heroic_resources_path, executable)
        elif heroicconfig["defaultSettings"].get("altLegendaryBin") and gametype == "epic":

                binary = heroicconfig["defaultSettings"]["altLegendaryBin"]
        #elif 'altGogdlBin' in heroicconfig['defaultSettings'].keys() and heroicconfig["defaultSettings"]["altGogdlBin"] != "" and gametype != "epic":
        
                #binary = heroicconfig["defaultSettings"]["altGogdlBin"]
        else:#AppImage
            if "GameFiles" in os.getcwd():#select parent dir
                binary = os.path.join(os.path.dirname(os.getcwd()), "binaries", executable)
            else:
                binary = os.path.join(os.getcwd(), "binaries", executable)
            
        return binary
    except Exception:

        logging.critical(traceback.format_exc())
        if not args.silent:
            os.system('zenity --error --title="Process Failed" --text="\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
        sys.exit()