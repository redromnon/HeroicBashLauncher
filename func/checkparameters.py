#CHECKS/UPDATES PARAMETERS FOR A GAME - CHANGES FOR EPIC, GOG-LINUX & GOG-WINDOWS 

import os, json, sys, traceback, logging
from func import configpath
from func.checkbinary import getbinary


def checkparameters(appname, gamejsonfile, gametype):

  #Convert the game's json file to dict
  with open(gamejsonfile, encoding='utf-8') as g:
      game = json.load(g)

  #Check binary (Legendary or gogdl)
  binary = getbinary(gametype)

  #Check if parameters are present (launcherArgs, enviromentOptions, targetExe)  
  def ifpresent(parameter):

    if parameter in game[appname].keys():
      return True

  try:
    #CONFIGURING BOOLEAN PARAMETERS

    #audioFix
    audioFix = ""
    if ifpresent("audioFix"):

      if game[appname]["audioFix"]:
        audioFix = "PULSE_LATENCY_MSEC=60 "

    #print(audioFix)


    #Auto-Cloud Save Sync
    cloudsync = ""
    if ifpresent("autoSyncSaves"):

      if game[appname]["autoSyncSaves"]:
    
        if game[appname]["savesPath"] != "":
          #Download and Upload
          cloudsync = binary + 'sync-saves --save-path "' + game[appname]["savesPath"] + '" ' + appname + ' -y '

    #print(cloudsync)


    #enableEsync (Wine, Proton)
    enableEsync = ["","PROTON_NO_ESYNC=1 "]
    if ifpresent("enableEsync"):

      if game[appname]["enableEsync"]:
        enableEsync[0] = "WINEESYNC=1 "
        enableEsync[1] = ""

    #print(enableEsync)


    #enableFsync (Wine, Proton)
    enableFsync = ["", "PROTON_NO_FSYNC=1 "]
    if ifpresent("enableFsync"):

      if game[appname]["enableFsync"]:
        enableFsync[0] = "WINEFSYNC=1 "
        enableFsync[1] = ""

    #print(enableFsync)


    #enableFSR & Sharpness
    enableFSR = ""
    maxSharpness = ""
    if ifpresent("enableFSR"):

      if game[appname]["enableFSR"]:
        enableFSR = "WINE_FULLSCREEN_FSR=1 "
        maxSharpness = "WINE_FULLSCREEN_FSR_STRENGTH=" + str(game[appname]["maxSharpness"]) + " " 

    #print(enableFSR)


    #enableResizableBar
    enableResizableBar = ""
    if ifpresent("enableResizableBar"):

      if game[appname]["enableResizableBar"]:
        enableResizableBar = "VKD3D_CONFIG=upload_hvv "

    #print(enableResizableBar)


    #nvidiaPrime
    nvidiaPrime = ""
    if ifpresent("nvidiaPrime"):

      if game[appname]["nvidiaPrime"]:
        nvidiaPrime = "DRI_PRIME=1 __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia "

    #print(nvidiaPrime)


    #offlineMode
    offlineMode = ""
    if ifpresent("offlineMode"):

      if game[appname]["offlineMode"]:
        offlineMode = "--offline "

    #offlineMode parameter when no internet connection
    force_offlineMode = "--offline "

    #print(offlineMode)


    #showFps
    showFps = ""
    if ifpresent("showFps"):

      if game[appname]["showFps"]:
        showFps = "DXVK_HUD=fps "

    #print(showFps)


    #showMangohud
    showMangohud = ""
    if ifpresent("showMangohud"):

      if game[appname]["showMangohud"]:
        showMangohud = "mangohud --dlsym "

    #print(showMangohud)


    #useGameMode
    useGameMode = ""
    if ifpresent("useGameMode"): 
  
      if game[appname]["useGameMode"]:
        useGameMode = "gamemoderun "

    #print(useGameMode)


    #EAC runtime
    eacRuntime = ""
    if ifpresent("eacRuntime"): 
  
      if game[appname]["eacRuntime"]:
        eacRuntime = configpath.runtimepath + "eac_runtime "

    
    #battlEye runtime
    battlEyeRuntime = ""
    if ifpresent("battlEyeRuntime"): 
  
      if game[appname]["battlEyeRuntime"]:
        battlEyeRuntime = configpath.runtimepath + "battleye_runtime "


    #CONFIGURING OTHER PARAMETERS

    #language
    language = ""
    if ifpresent("language"):

      if game[appname]["language"] == "":

        #Use Heroic's language setting if game setting lang not specified
        with open(configpath.storejsonpath, encoding='utf-8') as l:
          storejson = json.load(l)

        language = "--language " + storejson["language"] + " "
      else:
        language = "--language " + game[appname]["language"] + " "

    #launcherArgs
    launcherArgs = "" #Declared this because of reference assignment error
    if ifpresent("launcherArgs"):

      if game[appname]["launcherArgs"] == "":
        launcherArgs = ""
      else:
        launcherArgs = game[appname]["launcherArgs"] + " "

      #print(launcherArgs)

    #wrapperOptions
    wrapperOptions = "LD_PRELOAD= " 
    if ifpresent("wrapperOptions"):

      for i in game[appname]["wrapperOptions"]:
        wrapperOptions = wrapperOptions +  i["exe"] + " " + i["args"] + " "


    #enviromentOptions
    enviromentOptions = ""
    if ifpresent("enviromentOptions"):

      for i in game[appname]["enviromentOptions"]:
        enviromentOptions = enviromentOptions +  i["key"] + "=" + i["value"] + " "

      #print(enviromentOptions)


    #targetExe
    targetExe = ""
    if ifpresent("targetExe"):

      if game[appname]["targetExe"] == "":
        targetExe = ""
      else:
        targetExe = '--override-exe "' + game[appname]["targetExe"] + '" '

      #print(targetExe)


    #Steam Runtime
    steam_runtime = ""
    steam_runtime_win = False
    if ifpresent("useSteamRuntime"):

      if game[appname]["useSteamRuntime"]:

        #Scout
        if gametype == "gog-linux":
        
          if configpath.is_steam_flatpak:

            steam_runtime = os.path.expanduser("~") + "/.var/app/com.valvesoftware.Steam/data/Steam/ubuntu12_32/steam-runtime/run.sh "
          else:
            
            steam_runtime = os.path.expanduser("~") + "/.steam/root/ubuntu12_32/steam-runtime/run.sh "

        #Soldier
        else:
          steam_runtime_win = True

          if configpath.is_steam_flatpak:

            steam_runtime = os.path.expanduser("~") + "/.var/app/com.valvesoftware.Steam/steamapps/common/SteamLinuxRuntime_soldier/_v2-entry-point -- "
          else:
            
            steam_runtime = os.path.expanduser("~") + "/.steam/root/steamapps/common/SteamLinuxRuntime_soldier/_v2-entry-point -- "

      #print(targetExe)


    #Get GOG game's installed location
    if gametype != "epic":

      #Path to installed games via gog's installed.json file
      #goginstalledpath = os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"

      with open(configpath.goginstalledpath, encoding='utf-8') as l:
        goginstalled = json.load(l)

      goginstalledkeyarray = list(goginstalled['installed'])

      #Get install location
      game_loc = ""
      for i in goginstalledkeyarray:

        if appname == i['appName']:

          game_loc = '"' + i['install_path'] + '" '
          break



    #ADD IF-ELSE FOR GOG(LINUX OR WIN) AND EPIC
    if gametype == "epic" or gametype == "gog-win":

      #winePrefix
      winePrefix = ""
      if ifpresent("winePrefix"):
        winePrefix = game[appname]["winePrefix"]

      #print(winePrefix)


      #wineVersion (IMPACTS LAUNCH COMMAND)

      #wine bin & name 
      try:
        wineVersion_bin = game[appname]["wineVersion"]["bin"]
        wineVersion_name = game[appname]["wineVersion"]["name"]
      except:
        logging.warning("No wineVersion key found. Defaulting wine version to the one used in Heroic's global settings...")
        #Use default wine version used in global settings 
        with open(configpath.heroicconfigpath, encoding='utf-8') as p:
            heroicconfig = json.load(p)

        wineVersion_bin = heroicconfig["defaultSettings"]["wineVersion"]["bin"]
        wineVersion_name = heroicconfig["defaultSettings"]["wineVersion"]["name"]



      #name(IMPORTANT)

      if "Wine" in wineVersion_name:

        bin = "--wine " + wineVersion_bin + " "
        wineprefix = '--wine-prefix "' + winePrefix + '" '

        if gametype == "epic":

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync[0] + enableFsync[0] + enableResizableBar + enviromentOptions + nvidiaPrime + wrapperOptions + eacRuntime + battlEyeRuntime + showMangohud + useGameMode + binary + "launch " + appname + " " + language + targetExe + offlineMode + bin + wineprefix + launcherArgs
        elif gametype == "gog-win":#Windows GOG

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync[0] + enableFsync[0] + enableResizableBar + enviromentOptions + nvidiaPrime + wrapperOptions + eacRuntime + battlEyeRuntime + showMangohud + useGameMode + binary + "launch " + game_loc + appname + " " + targetExe + offlineMode + bin + wineprefix + "--os windows " + launcherArgs
      elif "Proton" in wineVersion_name:

        if configpath.is_flatpak == False:
          steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + os.path.expanduser("~") + "/.steam/steam "
        else:
          steamclientinstall = "STEAM_COMPAT_CLIENT_INSTALL_PATH=" + os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/.steam/steam "
        
        steamcompactdata = 'STEAM_COMPAT_DATA_PATH="' + winePrefix + '" '
        
        #Wrap Proton path (bin) in quotes to avoid errors due to spaces in the path
        wineVersion_bin = "'" + wineVersion_bin + "'"

        #Check if Steam Soldier runtime is enabled
        if steam_runtime_win:
          bin = '--no-wine --wrapper "' + steam_runtime + wineVersion_bin + ' waitforexitandrun" '
          steamappid = 'SteamAppId=0 '
        else:
          bin = '--no-wine --wrapper "' + wineVersion_bin + ' run" '
          steamappid = ''

        if gametype == "epic":

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync[1] + enableFsync[1] + enableResizableBar + enviromentOptions + steamappid + nvidiaPrime + steamclientinstall + steamcompactdata + wrapperOptions + eacRuntime + battlEyeRuntime + showMangohud + useGameMode + binary + "launch " + appname + " " + language + targetExe + offlineMode + bin + launcherArgs
        elif gametype == "gog-win":#Windows GOG

          launchcommand = audioFix + showFps + enableFSR + maxSharpness + enableEsync[1] + enableFsync[1] + enableResizableBar + enviromentOptions + steamappid + nvidiaPrime + steamclientinstall + steamcompactdata + wrapperOptions + eacRuntime + battlEyeRuntime + showMangohud + useGameMode + binary + "launch " + game_loc + appname + " " + targetExe + offlineMode + bin + "--os windows " + launcherArgs
    else:#LINUX GOG

      launchcommand = audioFix + showFps + enviromentOptions + nvidiaPrime + wrapperOptions + showMangohud + useGameMode + steam_runtime + binary + "launch " + game_loc + appname + " " + targetExe + offlineMode + "--platform=linux " + launcherArgs
  except Exception:

      logging.critical(traceback.format_exc())
      os.system('zenity --error --title="Process Failed" --text="\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
      sys.exit()

  #The entire launch command
  #print(launchcommand)

  #Return as list
  return [launchcommand, cloudsync]
