#TO USE LEGENDARY OR GOGDL
#   For AppImage, check if alternavtive binary (Legendary) is added.
#   If not, check folder under /tmp/ that includes path to the binaries.

import os, json, sys

def getbinary(gametype):

    try:

        #Path to heroic's configuration json file
        heroicconfigpath = os.path.expanduser("~") + "/.config/heroic/config.json"

        #Path to tmp dir
        list = os.listdir('/tmp/')

        #Convert config json to dict
        with open(heroicconfigpath) as p:
            heroicconfig = json.load(p)

        #Checking
        if os.path.exists("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux") == True:

            if gametype != "epic":
                binary = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/gogdl "
            else:
                binary = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary "   

        elif heroicconfig["defaultSettings"]["altLegendaryBin"] != "":
            binary = heroicconfig["defaultSettings"]["altLegendaryBin"] + " "
        else:

            for i in list:
                if "Heroic" in i:
                    
                    if gametype != "epic":
                        binary = '/tmp/' + i + '/resources/app.asar.unpacked/build/bin/linux/gogdl '
                    else:
                        binary = '/tmp/' + i + '/resources/app.asar.unpacked/build/bin/linux/legendary '
                    break

        return binary
    except:
        os.system('zenity --error --title="Failed" --text="Looks like you are using Heroic via AppImage\n\nMake sure to keep Heroic running and try again" --width=300')
        sys.exit()