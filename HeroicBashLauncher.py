
import os, glob, json, time
from func.gameName import getnameofgame

#GETTING PATH OF PRESENT DIRECTORY
programfolderpath = os.getcwd()


#ASSIGNING PATH TO HEROIC GAMES CONFIG FILE
homeuser = os.path.expanduser("~")
path = homeuser + "/.config/heroic/GamesConfig"
os.chdir(path)
#print(os.getcwd())
print()


#GLOBAL VARIABLES
global heroic # Heroic's legendary launch
heroic = "/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary "

global legendaryinstalledpath # List of installed games
legendaryinstalledpath = homeuser + "/.config/legendary/installed.json"



#THE BODY PART
#####################################################################

#CREATING GAME LAUNCH (.sh) FILES
def launchfile(game):


  #Converting keys intro array to get game alias
  gamekeyarray = list(game.keys()) #Keys to array 
  appname = gamekeyarray[0] #First index contains the game's AppName

  #################################

  #FINDING TITLE NAME OF THE GAME
  def findgamename(appname): 

    #Convert the json file into a dictionary called installed
    with open(legendaryinstalledpath) as f:
      installed = json.load(f) 

    #Finding the game's title name
    realgamename = installed[appname]["title"]
    #print(realgamename)

    return realgamename

  #################################

  realgamename = findgamename(appname)

  print("\nPreparing " + realgamename + "....")


  #################################

  #CREATING THE LAUNCH FILE

  def gameFile(launchcommand, offline_launchcommand, cloudsync):
    
    #Generating game's name without special characters
    simplified_gamename = getnameofgame(realgamename)

    #Creating the game file name
    gameFile = programfolderpath + "/GameFiles/" + simplified_gamename + ".sh"

    #Offline Dialog
    offline_dialog= 'zenity --warning --title="Offline" --text="Cannot connect to Epic servers. Running game in offline mode." --width=200 --timeout=2'

    #Creating game file
    with open(gameFile, "w") as g:
        g.write('#!/bin/bash \n\n' + '#Game Name = ' + realgamename + '\n\n' + '#App Name (Legendary) = ' + appname + '\n\n' + 'cd .. && python3 HeroicBashLauncher.py #Overrides launch parameters' + '\n\n' + cloudsync + '\n\n' + launchcommand + '|| ( ' + offline_dialog + ' ; ' + offline_launchcommand + ')')

    #Making the file executable
    os.system("chmod u+x " + gameFile)


  ################################

  #Check if parameters are present (launcherArgs, otherOptions, targetExe)
  def ifpresent(parameter):

    if parameter in game[appname].keys():
      return True

  #CONFIGURING BOOLEAN PARAMETERS

  #audioFix
  audioFix = ""
  if ifpresent("audioFix") == True:

    if game[appname]["audioFix"] == True:
      audioFix = "PULSE_LATENCY_MSEC=60 "

  #print(audioFix)


  #Auto-Cloud Save Sync
  cloudsync = ""
  if ifpresent("autoSyncSaves") == True:

    if game[appname]["autoSyncSaves"] == True:
    
      if game[appname]["savesPath"] == "":
        cloudsync = ""
      else:
        cloudsync = heroic + 'sync-saves --save-path "' + game[appname]["savesPath"] + '" ' + appname + ' -y '

  #print(cloudsync)


  #enableEsync
  enableEsync = ""
  if ifpresent("enableEsync") == True:

    if game[appname]["enableEsync"] == True:
      enableEsync = "WINEESYNC=1 "

  #print(enableEsync)


  #enableFsync
  enableFsync = ""
  if ifpresent("enableFsync") == True:

    if game[appname]["enableFsync"] == True:
      enableFsync = "WINEFSYNC=1 "

  #print(enableFsync)


  #enableFSR & Sharpness
  enableFSR = ""
  maxSharpness = ""
  if ifpresent("enableFSR") == True:

    if game[appname]["enableFSR"] == True:
      enableFSR = "WINE_FULLSCREEN_FSR=1 "
      maxSharpness = "WINE_FULLSCREEN_FSR_STRENGTH=" + str(game[appname]["maxSharpness"]) + " " 

  #print(enableFSR)


  #enableResizableBar
  enableResizableBar = ""
  if ifpresent("enableResizableBar") == True:

    if game[appname]["enableResizableBar"] == True:
      enableResizableBar = "VKD3D_CONFIG=upload_hvv "

  #print(enableResizableBar)


  #nvidiaPrime
  nvidiaPrime = ""
  if ifpresent("nvidiaPrime") == True:

    if game[appname]["nvidiaPrime"] == True:
      nvidiaPrime = "__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia "

  #print(nvidiaPrime)


  #offlineMode
  offlineMode = ""
  if ifpresent("offlineMode") == True:

    if game[appname]["offlineMode"] == True:
      offlineMode = "--offline "

  #offlineMode parameter when no internet connection
  force_offlineMode = "--offline "

  #print(offlineMode)


  #showFps
  showFps = ""
  if ifpresent("showFps") == True:

    if game[appname]["showFps"] == True:
      showFps = "DXVK_HUD=fps "

  #print(showFps)


  #showMangohud
  showMangohud = ""
  if ifpresent("showMangohud") == True:

    if game[appname]["showMangohud"] == True:
      showMangohud = "mangohud --dlsym "

  #print(showMangohud)


  #useGameMode
  useGameMode = ""
  if ifpresent("useGameMode") == True: 
  
    if game[appname]["useGameMode"] == True:
      useGameMode = "/usr/bin/gamemoderun "

  #print(useGameMode)



  #CONFIGURING OTHER PARAMETERS


  #launcherArgs
  launcherArgs = "" #Declared this because of reference assignment error
  if ifpresent("launcherArgs") == True:

    if game[appname]["launcherArgs"] == "":
      launcherArgs = ""
    else:
      launcherArgs = game[appname]["launcherArgs"] + " "

    #print(launcherArgs) 


  #otherOptions
  otherOptions = ""
  if ifpresent("otherOptions") == True:

    if game[appname]["otherOptions"] == "":
      otherOptions = ""
    else:
      otherOptions = game[appname]["otherOptions"] + " "

    #print(otherOptions)


  #targetExe
  targetExe = ""
  if ifpresent("targetExe") == True:

    if game[appname]["targetExe"] == "":
      targetExe = ""
    else:
      targetExe = "--override-exe " + game[appname]["targetExe"] + " "

    #print(targetExe)



  #winePrefix
  winePrefix = game[appname]["winePrefix"]

  #print(winePrefix)


  #wineVersion (IMPACTS LAUNCH COMMAND)

  #bin 
  wineVersion_bin = game[appname]["wineVersion"]["bin"]

  #print(wineVersion_bin)


  #name(IMPORTANT)

  launchcommand = " "
  launchgame = "launch " + appname + " " 

  if "Proton" in game[appname]["wineVersion"]["name"]:

    steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + homeuser + "/.steam/steam "
    steamcompactdata = "STEAM_COMPAT_DATA_PATH='" + winePrefix + "' "
    bin = '--no wine --wrapper "' + wineVersion_bin + ' run" '

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + launcherArgs
    offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + force_offlineMode + bin + launcherArgs

  elif "Wine" in game[appname]["wineVersion"]["name"]:

    bin = "--wine " + wineVersion_bin + " "
    wineprefix = "--wine-prefix '" + winePrefix + "' "

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + wineprefix + launcherArgs
    offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + heroic + launchgame + targetExe + force_offlineMode + bin + wineprefix + launcherArgs


  #The entire launch command
  #print(launchcommand)

  #Now create the file
  gameFile(launchcommand,offline_launchcommand, cloudsync)
  print("Done!")



#####################################################################



#FINDING THE INSTALLED GAME FILES & GENERATING LAUNCH FILE PER GAME

print("Generating a list of installed games... ")


#Clean leftover files
print("\nCleaning left over game files if any...")
os.system("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary cleanup")



listofgames = glob.glob('./*.json') # List of all available .json game files

l = len(listofgames) # No. of games


#EXIT the program if no games are found
if l == 0:
  print("No games installed...\nCouldn't create game launch files.")
  exit()

i = 0

################################
#Convert the legendary installed.json file into a dictionary called installed
with open(legendaryinstalledpath) as f:
  installed = json.load(f)

#Converting "installed" keys into array to get game alias
installedkeyarray = list(installed.keys())

################################
#launchfile(list[7])

print("\n\nDone! Now creating launch files...\n")

#Loop for generating launch commands for each installed game 
while i != l:
	
  #Convert the json file into a dictionary called game
  with open(listofgames[i]) as f:
    game = json.load(f)

  checkList = list(game.keys()) # Keys into array contaning - Name of the game, version and explicit
  	
  #Check if game is installed
  if "version" in checkList:

    if checkList[0] in installedkeyarray:
    
      launchfile(game) # Call the main function
	
  i = i+1


#####################################


#END OF THE PROGRAM
print("\n...Process finished. Launch files stored in GameFiles folder.\nHave fun gaming!")
#time.sleep(1.5) wait for 1.5 seconds and then end
