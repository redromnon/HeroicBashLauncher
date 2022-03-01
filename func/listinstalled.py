#List installed games

import os, json
from legendaryclean import legendaryclean
from createlaunchfile import createlaunchfile

def listinstalled():

    #Path to heroic's GamesConfig dir where each installed game's json is stored
    gamesjsonpath = os.path.expanduser("~") + "/.config/heroic/GamesConfig"

  #EPIC GAMES LIBRARY
  #------------------------------------------------------------------------------------

    #legendary cleanup
    legendaryclean()

    #Path to installed games via legendary's installed.json file
    legendaryinstalledpath = os.path.expanduser("~") + "/.config/legendary/installed.json"

    #Convert legendary json to dict
    with open(legendaryinstalledpath) as l:
      installed = json.load(l) 

    #Games' AppNames stored in list 
    installedkeyarray = list(installed.keys())

    # Moving one directory up
    #os.chdir(os.path.dirname(os.getcwd()))
    #print(os.getcwd())

    #Proceed to making launch files
    print("\n\nDone! Now creating launch files for your Epic Games library ...\n")
    for i in installedkeyarray:

        #Print current action
        print(installed[i]["title"] + " [" + i + "]...\n") # installed[i] = game's name, i = game's appname

        #Pointing to the game's json file
        gamejson = gamesjsonpath + "/" + i + ".json"

        #Removing special characters from the game name (Steam issue)
        gamename = installed[i]["title"].encode("ascii", "ignore")

        #Preparing launch file
        createlaunchfile(gamename.decode(), i, gamejson, "epic") # gamename, appname, game's json file path

  #GOG LIBRARY
  #------------------------------------------------------------------------------------
    if os.path.exists(os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"):

      #Path to installed games via gog's installed.json file
      goginstalledpath = os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"

      #Path to all games info via gog's library.json file
      goglibrarypath = os.path.expanduser("~") + "/.config/heroic/gog_store/library.json"

      #Convert both json to dict
      with open(goginstalledpath) as l:
        goginstalled = json.load(l)

      with open(goglibrarypath) as p:
        goglibrary = json.load(p) 

      #Stored as list 
      goginstalledkeyarray = list(goginstalled['installed'])
      goglibrarykeyarray = list(goglibrary['games'])

      #Proceed to making launch files
      print("\n\nDone! Now creating launch files for your GOG library ...\n")
      for i in goginstalledkeyarray:

        for j in goglibrarykeyarray:

          if i['appName'] == j['app_name']:

            #Print current action
            print(j['title'] + " [" + i['appName'] + "]...\n")

            #Pointing to the game's json file
            gamejson = gamesjsonpath + "/" + j['app_name'] + ".json"

            #Removing special characters from the game name (Steam issue)
            gamename = j['title'].encode("ascii", "ignore")

            #Check if game is linux or windows
            if i['platform'] == "linux":
              gametype = "gog-linux"
            else:
              gametype = "gog-win"

            #Preparing launch file
            createlaunchfile(gamename.decode(), j['app_name'], gamejson, gametype) # gamename, appname, game's json file path

    #END OF THE PROGRAM
    print("\n...Process finished. Launch files stored in GameFiles folder.\nHave fun gaming!")