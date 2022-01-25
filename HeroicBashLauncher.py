
import os, glob, json, time


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
  gamename = gamekeyarray[0] #First index contains the game's name

  #################################

  #FINDING TITLE NAME OF THE GAME
  def findgamename(gamename): 

    #Convert the json file into a dictionary called installed
    with open(legendaryinstalledpath) as f:
      installed = json.load(f) 

    #Finding the game's title name
    realgamename = installed[gamename]["title"]
    #print(realgamename)

    return realgamename

  #################################

  realgamename = findgamename(gamename)

  print("\nPreparing " + realgamename + "....")


  #################################

  #CREATING THE LAUNCH FILE

  def gameFile(launchcommand, offline_launchcommand, cloudsync):
    
    #Creating the game file name
    gameFile = programfolderpath + "/GameFiles/" + gamename + ".sh"

    #Offline Dialog
    offline_dialog= 'zenity --warning --title="Offline" --text="Cannot connect to Epic servers. Running game in offline mode." --width=200 --timeout=2'

    #Creating game file
    with open(gameFile, "w") as g:
        g.write('#!/bin/bash \n\n' + '#Game Name = ' + realgamename + '\n\n' + 'cd .. && python3 HeroicBashLauncher.py #Overrides launch parameters' + '\n\n' + cloudsync + '\n\n' + launchcommand + '|| ( ' + offline_dialog + ' ; ' + offline_launchcommand + ')')

    #Making the file executable
    os.system("chmod u+x " + gameFile)


  ################################

  #Check if parameters are present (launcherArgs, otherOptions, targetExe)
  def ifpresent(parameter):

    if parameter in game[gamename].keys():
      return True

  #CONFIGURING BOOLEAN PARAMETERS

  #audioFix
  audioFix = ""
  if ifpresent("audioFix") == True:

    if game[gamename]["audioFix"] == True:
      audioFix = "PULSE_LATENCY_MSEC=60 "

  #print(audioFix)


  #Auto-Cloud Save Sync
  cloudsync = ""
  if ifpresent("autoSyncSaves") == True:

    if game[gamename]["autoSyncSaves"] == True:
    
      if game[gamename]["savesPath"] == "":
        cloudsync = ""
      else:
        cloudsync = heroic + 'sync-saves --save-path "' + game[gamename]["savesPath"] + '" ' + gamename + ' -y '

  #print(cloudsync)


  #enableEsync
  enableEsync = ""
  if ifpresent("enableEsync") == True:

    if game[gamename]["enableEsync"] == True:
      enableEsync = "WINEESYNC=1 "

  #print(enableEsync)


  #enableFsync
  enableFsync = ""
  if ifpresent("enableFsync") == True:

    if game[gamename]["enableFsync"] == True:
      enableFsync = "WINEFSYNC=1 "

  #print(enableFsync)


  #enableFSR & Sharpness
  enableFSR = ""
  maxSharpness = ""
  if ifpresent("enableFSR") == True:

    if game[gamename]["enableFSR"] == True:
      enableFSR = "WINE_FULLSCREEN_FSR=1 "
      maxSharpness = "WINE_FULLSCREEN_FSR_STRENGTH=" + str(game[gamename]["maxSharpness"]) + " " 

  #print(enableFSR)


  #enableResizableBar
  enableResizableBar = ""
  if ifpresent("enableResizableBar") == True:

    if game[gamename]["enableResizableBar"] == True:
      enableResizableBar = "VKD3D_CONFIG=upload_hvv "

  #print(enableResizableBar)


  #nvidiaPrime
  nvidiaPrime = ""
  if ifpresent("nvidiaPrime") == True:

    if game[gamename]["nvidiaPrime"] == True:
      nvidiaPrime = "__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia "

  #print(nvidiaPrime)


  #offlineMode
  offlineMode = ""
  if ifpresent("offlineMode") == True:

    if game[gamename]["offlineMode"] == True:
      offlineMode = "--offline "

  #offlineMode parameter when no internet connection
  force_offlineMode = "--offline "

  #print(offlineMode)


  #showFps
  showFps = ""
  if ifpresent("showFps") == True:

    if game[gamename]["showFps"] == True:
      showFps = "DXVK_HUD=fps "

  #print(showFps)


  #showMangohud
  showMangohud = ""
  if ifpresent("showMangohud") == True:

    if game[gamename]["showMangohud"] == True:
      showMangohud = "mangohud --dlsym "

  #print(showMangohud)


  #useGameMode
  useGameMode = ""
  if ifpresent("useGameMode") == True: 
  
    if game[gamename]["useGameMode"] == True:
      useGameMode = "/usr/bin/gamemoderun "

  #print(useGameMode)



  #CONFIGURING OTHER PARAMETERS


  #launcherArgs
  launcherArgs = "" #Declared this because of reference assignment error
  if ifpresent("launcherArgs") == True:

    if game[gamename]["launcherArgs"] == "":
      launcherArgs = ""
    else:
      launcherArgs = game[gamename]["launcherArgs"] + " "

    #print(launcherArgs) 


  #otherOptions
  otherOptions = ""
  if ifpresent("otherOptions") == True:

    if game[gamename]["otherOptions"] == "":
      otherOptions = ""
    else:
      otherOptions = game[gamename]["otherOptions"] + " "

    #print(otherOptions)


  #targetExe
  targetExe = ""
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

  if "Proton" in game[gamename]["wineVersion"]["name"]:

    steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + homeuser + "/.steam/steam "
    steamcompactdata = "STEAM_COMPAT_DATA_PATH='" + winePrefix + "' "
    bin = '--no wine --wrapper "' + wineVersion_bin + ' run" '

    launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + offlineMode + bin + launcherArgs
    offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + heroic + launchgame + targetExe + force_offlineMode + bin + launcherArgs

  elif "Wine" in game[gamename]["wineVersion"]["name"]:

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
