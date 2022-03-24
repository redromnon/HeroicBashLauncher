#Cleans temorary files and leftovers

import os, json
import configpath

def legendaryclean():

    #Convert config json to dict
    with open(configpath.heroicconfigpath) as p:
        heroicconfig = json.load(p)

    #Clean leftover files
    print("\nCleaning left over game files if any...")

    if os.path.exists("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux") == True:

            os.system("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary cleanup")
    elif heroicconfig["defaultSettings"]["altLegendaryBin"] != "":

            os.system(heroicconfig["defaultSettings"]["altLegendaryBin"] + " cleanup")
    else:#AppImage
            os.system(os.getcwd() + "/binaries/legendary cleanup")
