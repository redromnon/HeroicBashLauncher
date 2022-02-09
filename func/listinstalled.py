#List installed games

import os, json
from legendaryclean import legendaryclean
from createlaunchfile import createlaunchfile

def listinstalled():

    #legendary cleanup
    legendaryclean()

    #Path to installed games via legendary's installed.json file
    legendaryinstalledpath = os.path.expanduser("~") + "/.config/legendary/installed.json"

    #Path to heroic's GamesConfig dir where each installed game's json is stored
    heroicjsonpath = os.path.expanduser("~") + "/.config/heroic/GamesConfig"

    #Convert legendary json to dict
    with open(legendaryinstalledpath) as l:
      installed = json.load(l) 

    #Games' AppNames stored in list 
    installedkeyarray = list(installed.keys())

    # Moving one directory up
    #os.chdir(os.path.dirname(os.getcwd()))
    #print(os.getcwd())

    #Proceed to making launch files
    print("\n\nDone! Now creating launch files for the following games...\n")
    for i in installedkeyarray:

        #Print current action
        print(installed[i]["title"] + " [" + i + "]...\n") # installed[i] = game's name, i = game's appname

        #Pointing to the game's json file
        gamejson = heroicjsonpath + "/" + i + ".json"

        createlaunchfile(installed[i]["title"], i, gamejson) # gamename, appname, game's json file path

    #END OF THE PROGRAM
    print("\n...Process finished. Launch files stored in GameFiles folder.\nHave fun gaming!")