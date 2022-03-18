#List installed games

import os, json
import configpath
from legendaryclean import legendaryclean
from createlaunchfile import createlaunchfile

def listinstalled():

    #Path to heroic's GamesConfig dir where each installed game's json is stored
    #gamesjsonpath = os.path.expanduser("~") + "/.config/heroic/GamesConfig"

  #EPIC GAMES LIBRARY
  #------------------------------------------------------------------------------------

    #legendary cleanup
    legendaryclean()

    #Path to installed games via legendary's installed.json file
    #legendaryinstalledpath = os.path.expanduser("~") + "/.config/legendary/installed.json"

    #Convert legendary json to dict
    with open(configpath.legendaryinstalledpath, encoding='utf-8') as l:
      installed = json.load(l) 

    #Games' AppNames stored in list 
    installedkeyarray = list(installed.keys())

    # Moving one directory up
    #os.chdir(os.path.dirname(os.getcwd()))
    #print(os.getcwd())

    #Proceed to making launch files
    print("\n\nDone! Now creating launch files for your Epic Games library ...\n")
    for i in installedkeyarray:
      
      #Make sure the entries are games, not DLC
      if installed[i]["is_dlc"] == False:

        #Removing special characters from the game name (Steam issue)
        gamename = installed[i]["title"].encode("ascii", "ignore")
        
        #Print current action
        print(gamename.decode() + " [" + i + "]...\n") # installed[i] = game's name, i = game's appname

        #Pointing to the game's json file
        gamejson = configpath.gamesjsonpath + "/" + i + ".json"

        #Preparing launch file
        createlaunchfile(gamename.decode(), i, gamejson, "epic") # gamename, appname, game's json file path

  #GOG LIBRARY
  #------------------------------------------------------------------------------------
    if os.path.exists(configpath.goginstalledpath):

      #Path to installed games via gog's installed.json file
      #goginstalledpath = os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"

      #Path to all games info via gog's library.json file
      #goglibrarypath = os.path.expanduser("~") + "/.config/heroic/gog_store/library.json"

      #Convert both json to dict
      with open(configpath.goginstalledpath, encoding='utf-8') as l:
        goginstalled = json.load(l)

      with open(configpath.goglibrarypath, encoding='utf-8') as p:
        goglibrary = json.load(p) 

      #Stored as list 
      goginstalledkeyarray = list(goginstalled['installed'])
      goglibrarykeyarray = list(goglibrary['games'])

      #Proceed to making launch files
      print("\n\nDone! Now creating launch files for your GOG library ...\n")
      for i in goginstalledkeyarray:

        for j in goglibrarykeyarray:

          if i['appName'] == j['app_name']:

            #Removing special characters from the game name (Steam issue)
            gamename = j['title'].encode("ascii", "ignore")
            
            #Print current action
            print(gamename.decode() + " [" + i['appName'] + "]...\n")

            #Pointing to the game's json file
            gamejson = configpath.gamesjsonpath + "/" + j['app_name'] + ".json"

            #Check if game is linux or windows
            if i['platform'] == "linux":
              gametype = "gog-linux"
            else:
              gametype = "gog-win"

            #Preparing launch file
            createlaunchfile(gamename.decode(), j['app_name'], gamejson, gametype) # gamename, appname, game's json file path

    #END OF THE PROGRAM
    print("\n...Process finished. Launch files stored in GameFiles folder.\nHave fun gaming!")
