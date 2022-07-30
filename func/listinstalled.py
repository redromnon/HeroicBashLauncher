#List installed games

import os, json, logging
from func import configpath
from func.gameName import rspchar
from func.createlaunchfile import createlaunchfile
from func.steam import *
from func import settings

def AddToSteam(gamename):

  #If system is Steam Deck, add to Steam right away or add to Steam script
    if "deck" in os.path.expanduser("~"):
        addtosteam(gamename)
    else:
        addtoscript(gamename)



def listinstalled():

  #EPIC GAMES LIBRARY
  #------------------------------------------------------------------------------------
  if os.path.exists(configpath.legendaryinstalledpath) and settings.enable_epic:

    #Convert legendary json to dict
    with open(configpath.legendaryinstalledpath, encoding='utf-8') as l:
      installed = json.load(l) 

    #Games' AppNames stored in list 
    installedkeyarray = list(installed.keys())

    #Proceed to making launch files
    logging.info("Done! Now creating launch files for your Epic Games library ...")
    for i in installedkeyarray:
      
      #Make sure the entries are games, not DLC
      if installed[i]["is_dlc"] == False:

        #Removing special characters from the game name (Steam issue)
        gamename = rspchar(installed[i]["title"])
        
        #Print current action
        logging.info(gamename + " [" + i + "]...") # installed[i] = game's name, i = game's appname

        #Preparing launch file
        createlaunchfile(gamename, i, "epic") # gamename, appname, game type

        #Prepare adding game to Steam or AddToSteam script
        AddToSteam(gamename)
  else:
    logging.warning("Creating scripts for Epic games is disabled in settings.config")

  #GOG LIBRARY
  #------------------------------------------------------------------------------------
  if os.path.exists(configpath.goginstalledpath) and settings.enable_gog:

    #Convert both json to dict, gamename is stored in goglibrarypath
    with open(configpath.goginstalledpath, encoding='utf-8') as l:
      goginstalled = json.load(l)

    with open(configpath.goglibrarypath, encoding='utf-8') as p:
      goglibrary = json.load(p) 

    #Stored as list 
    goginstalledkeyarray = list(goginstalled['installed'])
    goglibrarykeyarray = list(goglibrary['games'])

    #Proceed to making launch files
    logging.info("Done! Now creating launch files for your GOG library ...")
    for i in goginstalledkeyarray:

      for j in goglibrarykeyarray:

        if i['appName'] == j['app_name'] and i['is_dlc'] == False:

          #Removing special characters from the game name (Steam issue)
          gamename = rspchar(j['title'])

          #Print current action
          logging.info(gamename + " [" + i['appName'] + "]...")

          #Check if game is linux or windows
          if i['platform'] == "linux":
            gametype = "gog-linux"
          else:
            gametype = "gog-win"

          #Preparing launch file
          createlaunchfile(gamename, j['app_name'], gametype) # gamename, appname, gametype

          #Prepare adding game to Steam or AddToSteam script
          AddToSteam(gamename)
  else:
    logging.warning("Creating scripts for GOG games is disabled in settings.config")

  #END OF THE PROGRAM
  logging.info("Process finished. Launch scripts stored in GameFiles folder.")
