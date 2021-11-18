#!/usr/bin/python3

import os
import glob
import json

#GETTING PATH OF PRESENT DICTORY
programfolderpath = os.getcwd()

#ASSIGNING PATH TO HEROIC GAMES CONFIG FILE
homeuser = os.path.expanduser("~")
path = homeuser + "/.config/heroic/GamesConfig"
os.chdir(path)
#print(os.getcwd())
print()



#THE BODY PART
#####################################################################

global heroic # Heroic's legendary launch

#CREATING GAME LAUNCH (.sh) FILES
def launchfile(list):

  #print(list)
 
  #Convert the json file into a dictionary called game
  with open(list) as f:
    game = json.load(f)


  #Converting keys intro array to get game alias
  gamekeyarray = [*game] #Keys to array 
  gamename = gamekeyarray[0] #First index contains the game's name

  print("\nPreparing " + gamename + "....")


  #################################

  #CREATING THE LAUNCH FILE

  def gameFile(launchcommand, cloudsync):
    
    #Creating the game file name
    gameFile = programfolderpath + "/GameFiles/" + gamename + ".sh"

    #Creating or opening the game file
    f = open(gameFile, "w")

    #Writing the contents
    f.write("#!/bin/bash \n\n" + cloudsync + "\n\n" + launchcommand)

    #Closing the file
    f.close()

    #Making the file executable
    os.system("chmod u+x " + gameFile)


  ################################

  #CONFIGURING BOOLEAN PARAMETERS

  #audioFix
  if game[gamename]["audioFix"] == True:
    audioFix = "PULSE_LATENCY_MSEC=60 "
  else:
    audioFix = ""

  #print(audioFix)


  #enableEsync
  if game[gamename]["enableEsync"] == True:
    enableEsync = "WINEESYNC=1 "
  else:
    enableEsync = ""

  #print(enableEsync)


  #enableFsync
  if game[gamename]["enableFsync"] == True:
    enableFsync = "WINEFSYNC=1 "
  else:
    enableFsync = ""

  #print(enableFsync)


  #enableFSR
  if game[gamename]["enableFSR"] == True:
    enableFSR = "WINE_FULLSCREEN_FSR=1 "
  else:
    enableFSR = ""

  #print(enableFSR)


  #enableResizableBar
  if game[gamename]["enableResizableBar"] == True:
    enableResizableBar = "VKD3D_CONFIG=upload_hvv "
  else:
    enableResizableBar = ""

  #print(enableResizableBar)


  #nvidiaPrime
  if game[gamename]["nvidiaPrime"] == True:
    nvidiaPrime = "__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia "
  else:
    nvidiaPrime = ""

  #print(nvidiaPrime)


  #offlineMode
  if game[gamename]["offlineMode"] == True:
    offlineMode = "--offline "
  else:
    offlineMode = ""

  #print(offlineMode)


  #showFps
  if game[gamename]["showFps"] == True:
    showFps = "DXVK_HUD=fps "
  else:
    showFps = ""

  #print(showFps)


  #showMangohud
  if game[gamename]["showMangohud"] == True:
    showMangohud = "MANGOHUD=1 "
  else:
    showMangohud = ""

  #print(showMangohud)


  #useGameMode
  if game[gamename]["useGameMode"] == True:
    useGameMode = "/usr/bin/gamemoderun "
  else:
    useGameMode = ""

  #print(useGameMode)



  #CONFIGURING OTHER PARAMETERS

  #Check if parameters are present (launcherArgs, otherOptions, targetExe)
  def ifpresent(parameter):

    if parameter in game[gamename].keys():
      return True



  #maxSharpness
  if game[gamename]["enableFSR"] == True:
    maxSharpness = "WINE_FULLSCREEN_FSR_STRENGTH=" + str(game[gamename]["maxSharpness"]) + " "
  else:
     maxSharpness = ""

  #print(maxSharpness)


  #launcherArgs
  global launcherArgs #Declared this because of reference assignment error
  if ifpresent("launcherArgs") == True:

    if game[gamename]["launcherArgs"] == "":
      launcherArgs = ""
    else:
      launcherArgs = game[gamename]["launcherArgs"]

    #print(launcherArgs) 


  #otherOptions
  if ifpresent("otherOptions") == True:

    if game[gamename]["otherOptions"] == "":
      otherOptions = ""
    else:
      otherOptions = game[gamename]["otherOptions"]

    #print(otherOptions)


  #targetExe
  if ifpresent("targetExe") == True:

    if game[gamename]["targetExe"] == "":
      targetExe = ""
    else:
      targetExe = "--override-exe " + game[gamename]["targetExe"] + " "

    #print(targetExe)



  #winePrefix
  winePrefix = game[gamename]["winePrefix"]

  #print(winePrefix)


  #wineVersion (IMPACTS LAUNCH COMMAND)

  #bin 
  wineVersion_bin = game[gamename]["wineVersion"]["bin"]

  #print(wineVersion_bin)


  #name(IMPORTANT)

  launchcommand = " "
  launchgame = "launch " + gamename + " " 
  heroic = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary "

  if "Proton" in game[gamename]["wineVersion"]["name"]:

    steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + homeuser + "/.steam/steam "
    steamcompactdata = "STEAM_COMPAT_DATA_PATH='" + winePrefix + "' "
    bin = '--no wine --wrapper "' + wineVersion_bin + ' run" '

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + launcherArgs
  
  elif "Wine" in game[gamename]["wineVersion"]["name"]:

    bin = "--wine " + wineVersion_bin + " "
    wineprefix = "--wine-prefix '" + winePrefix + "' "

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + wineprefix + launcherArgs


  #savesPath (CloudSync)
  if ifpresent("savesPath") == True:

    if game[gamename]["savesPath"] == "":
      cloudsync = ""
    else:
      cloudsync = heroic + "sync-saves " + gamename + " -y"

    #print(targetExe)


  #The entire launch command
  #print(launchcommand)

  #Now create the file
  gameFile(launchcommand, cloudsync)
  print("Done!")

#####################################################################

#FINDING THE INSTALLED GAME FILES & GENERATING LAUNCH FILE PER GAME

print("Generating a list of installed games... ")

list = glob.glob('./*.json') # List of all available .json game files

l = len(list)

i = 0

#launchfile(list[7])

print("Done! Now creating launch files...\n")
#Loop for generating launch commands for each installed game 
while i != l:
	
  with open(list[i]) as f:
    game = json.load(f)
  		
  		
  checkList = game.keys()	
  	
  #Check if game is installed
  if "version" in checkList:
    launchfile(list[i])
	
  i = i+1


#####################################


#END OF THE PROGRAM
print("\n...Process finished. Have fun gaming!")