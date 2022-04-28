#CHECKS/UPDATES PARAMETERS FOR A GAME - CHANGES FOR EPIC, GOG-LINUX & GOG-WINDOWS 

from distutils.command.config import config
import os, json, sys, traceback
import configpath
from checkbinary import getbinary


def checkparameters(appname, gamejsonfile, gametype):

  #Convert the game's json file to dict
  with open(gamejsonfile, encoding='utf-8') as g:
      game = json.load(g)

  #Check binary (Legendary or gogdl)
  binary = getbinary(gametype)

  #Check if parameters are present (launcherArgs, otherOptions, targetExe)  
  def ifpresent(parameter):

    if parameter in game[appname].keys():
      return True

  try:
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
          #Download and Upload
          cloudsync = [binary + 'sync-saves --skip-upload --save-path "' + game[appname]["savesPath"] + '" ' + appname + ' -y ', 
                      binary + 'sync-saves --skip-download --save-path "' + game[appname]["savesPath"] + '" ' + appname + ' -y ']

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
        nvidiaPrime = "DRI_PRIME=1 __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia "

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


    #Steam Runtime(GOG)
    steam_runtime = ""
    if ifpresent("useSteamRuntime") == True:

      if game[appname]["useSteamRuntime"] == True:
        
        if configpath.is_steam_flatpak == True:

          steam_runtime = os.path.expanduser("~") + "/.var/app/com.valvesoftware.Steam/data/Steam/ubuntu12_32/steam-runtime/run.sh "
        else:
          
          if os.path.exists(os.path.expanduser('~') + '.local/share/Steam') == True:

            steam_runtime = os.path.expanduser("~") + "/.local/share/Steam/ubuntu12_32/steam-runtime/run.sh "
          else:

            steam_runtime = os.path.expanduser("~") + "/.steam/debian-installation/ubuntu12_32/steam-runtime/run.sh "

      #print(targetExe)


    #Get GOG game's installed location
    if gametype != "epic":

      #Path to installed games via gog's installed.json file
      #goginstalledpath = os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"

      with open(configpath.goginstalledpath, encoding='utf-8') as l:
        goginstalled = json.load(l)

      goginstalledkeyarray = list(goginstalled['installed'])

      #Get install location
      for i in goginstalledkeyarray:

        if appname == i['appName']:

          game_loc = '"' + i['install_path'] + '" '
          break



    #ADD IF-ELSE FOR GOG(LINUX OR WIN) AND EPIC
    if gametype == "epic" or gametype == "gog-win":

      #winePrefix
      winePrefix = game[appname]["winePrefix"]

      #print(winePrefix)


      #wineVersion (IMPACTS LAUNCH COMMAND)

      #bin 
      wineVersion_bin = game[appname]["wineVersion"]["bin"]

      #print(wineVersion_bin)


      #name(IMPORTANT)

      if "Wine" in game[appname]["wineVersion"]["name"]:

        bin = "--wine " + wineVersion_bin + " "
        wineprefix = "--wine-prefix '" + winePrefix + "' "

        if gametype == "epic":

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + binary + "launch " + appname + " " + targetExe + offlineMode + bin + wineprefix + launcherArgs
          offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + binary + "launch " + appname + " " + targetExe + force_offlineMode + bin + wineprefix + launcherArgs
        elif gametype == "gog-win":#Windows GOG

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + binary + "launch " + game_loc + appname + " " + targetExe + offlineMode + bin + wineprefix + "--os windows " + launcherArgs
          offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + binary + "launch " + game_loc + appname + " " + targetExe + force_offlineMode + bin + wineprefix + "--os windows " + launcherArgs
      elif "Proton" in game[appname]["wineVersion"]["name"]:

        if configpath.is_flatpak == False:
          steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + os.path.expanduser("~") + "/.steam/steam "
        else:
          steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/.steam/steam "
        
        steamcompactdata = "STEAM_COMPAT_DATA_PATH='" + winePrefix + "' "
        bin = '--no-wine --wrapper "' + wineVersion_bin + ' run" '

        if gametype == "epic":

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + binary + "launch " + appname + " " + targetExe + offlineMode + bin + launcherArgs
          offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + binary + "launch " + appname + " " + targetExe + force_offlineMode + bin + launcherArgs
        elif gametype == "gog-win":#Windows GOG

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + binary + "launch " + game_loc + appname + " " + targetExe + offlineMode + bin + "--os windows " + launcherArgs
          offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + steamclientinstall + steamcompactdata + showMangohud + useGameMode + binary + "launch " + game_loc + appname + " " + targetExe + force_offlineMode + bin + "--os windows " + launcherArgs  
    else:#LINUX GOG

      launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + steam_runtime + binary + "launch " + game_loc + appname + " " + targetExe + offlineMode + "--platform=linux " + launcherArgs
      offline_launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync + enableFsync + enableResizableBar + otherOptions + nvidiaPrime + showMangohud + useGameMode + steam_runtime + binary + "launch " + game_loc + appname + " " + targetExe + force_offlineMode + "--platform=linux " + launcherArgs
  except Exception:

      print(traceback.format_exc())
      os.system('zenity --error --title="Process Failed" --text="\n\nPlease check game log for the error and consider reporting it as an issue on GitHub." --width=400')
      sys.exit()

  #The entire launch command
  #print(launchcommand)

  #Return as list
  return [launchcommand, offline_launchcommand, cloudsync]
