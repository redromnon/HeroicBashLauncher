#CHECKS/UPDATES PARAMETERS FOR A GAME - CHANGES FOR EPIC, GOG-LINUX & GOG-WINDOWS 

import os, json, sys, traceback, logging
import shlex
from func import configpath
from func import settings
from func.checkbinary import getbinary
from func import settings

def checkparameters(appname, gamejsonfile, gametype):
  """Checks the configuration parameters for the specified appname.
  Arguments and environment variables are based on the ones found in backend/launcher.ts and backend/legendary/games.ts:launch() in HeroicGamesLauncher.
  """

  environment = {}

  #Convert the game's json file to dict
  with open(gamejsonfile, encoding='utf-8') as g:
      gameSettings = json.load(g)[appname]

  #Check binary (Legendary or gogdl)
  binary = getbinary(gametype)

  try:
    #CONFIGURING BOOLEAN PARAMETERS

    #Auto-Cloud Save Sync
    cloudsync = ""
    if gameSettings.get("autoSyncSaves") and gameSettings.get("savesPath"):
          #Download and Upload
          cloudsync = f"{binary} sync-saves --save-path \"{gameSettings['savesPath']}\" {appname} -y"

    # Set environment variables first

    #showFps
    if gameSettings.get("showFps"):
        environment["DVXK_HUD"] = "fps"

    #DXVK FPS Limit
    if gameSettings.get("enableDXVKFpsLimit"): 
        environment["DXVK_FRAME_RATE"] = str(gameSettings.get("DXVKFpsCap")) if gameSettings.get("DXVKFpsCap") else "60"

    #enableFSR & Sharpness
    if gameSettings.get("enableFSR") and gameSettings.get("maxSharpness"):
        environment["WINE_FULLSCREEN_FSR"] = "1"
        environment["WINE_FULLSCREEN_FSR_STRENGTH"] = str(gameSettings.get("maxSharpness"))

    wrapperArgs = []
    #eacRuntime
    eacRuntimeArgs =  []
    if gameSettings.get("eacRuntime"): 
        environment["PROTON_EAC_RUNTIME"] = os.path.join(configpath.runtimepath, "eac_runtime")

    #battlEyeRuntime
    battlEyeRuntimeArgs = []
    if gameSettings.get("battlEyeRuntime"): 
        environment["PROTON_BATTLEYE_RUNTIME"] = os.path.join(configpath.runtimepath, "battleye_runtime")

    #nvidiaPrime
    if gameSettings.get("nvidiaPrime"):
        environment["DRI_PRIME"] = "1"
        environment["__NV_PRIME_RENDER_OFFLOAD"] = "1"
        environment["__GLX_VENDOR_LIBRARY_NAME"] = "nvidia"

    #enviromentOptions (spelled this way in Heroic)
    if gameSettings.get("enviromentOptions"):
      for option in gameSettings["enviromentOptions"]:
        environment[option["key"]] = str(option["value"])
    
    # Set LD_PRELOAD if it is not set, fixes an error in some games.
    if not os.environ.get("LD_PRELOAD") and not environment.get("LD_PRELOAD"):
      environment["LD_PRELOAD"] = ''

    #wrapperOptions
    if gameSettings.get("wrapperOptions"):
      for wrapperEntry in gameSettings["wrapperOptions"]:
        wrapperArgs.append(wrapperEntry["exe"])
        if wrapperEntry.get("args"):
          wrapperArgs += shlex.split(wrapperEntry["args"])

    #showMangohud
    showMangoHudArgs = []
    if gameSettings.get("showMangohud"):
        
      if not configpath.is_flatpak:
        environment["MANGOHUD_CONFIGFILE"] = os.path.join(os.path.expanduser('~'), '.config/MangoHud/MangoHud.conf')

      showMangoHudArgs = ["mangohud", "--dlsym"]
    wrapperArgs += showMangoHudArgs

    #useGameMode
    useGameModeArgs = []
    if gameSettings.get("useGameMode"): 
        useGameModeArgs = ["gamemoderun"]
    wrapperArgs += useGameModeArgs


    #CONFIGURING OTHER PARAMETERS

    #offlineMode
    offlineModeArgs = []
    if gameSettings.get("offlineMode") or settings.isoffline:
      offlineModeArgs.append("--offline")

    #language
    languageCode = gameSettings.get("language")
    if not languageCode:
        #Use Heroic's language setting if game setting lang not specified
        with open(configpath.storejsonpath, encoding='utf-8') as l:
          configStore = json.load(l)
        languageCode = configStore.get("language")

    languageArgs = ["--language", languageCode] if languageCode else []


    #launcherArgs
    launcherArgs = []
    if gameSettings.get("launcherArgs"):
        launcherArgs += shlex.split(gameSettings["launcherArgs"])


    #targetExe
    targetExeArgs = []
    if gameSettings.get("targetExe"):
        targetExeArgs = ['--override-exe', f"\"{gameSettings['targetExe']}\""]

    #Steam Runtime
    steam_runtime_win = False
    steamRuntimeBinArgs = []
    if gameSettings.get("useSteamRuntime"):

        #Scout
        if gametype == "gog-linux":
        
          if configpath.is_steam_flatpak:

            steamRuntimeBinArgs = [ os.path.expanduser("~/.var/app/com.valvesoftware.Steam/data/Steam/ubuntu12_32/steam-runtime/run.sh") ]
          else:
            steamRuntimeBinArgs = [ os.path.expanduser("~/.steam/root/ubuntu12_32/steam-runtime/run.sh")]

        #Soldier
        else:
          steam_runtime_win = True

          if configpath.is_steam_flatpak:

            steamRuntimeBinArgs = [ os.path.expanduser("~/.var/app/com.valvesoftware.Steam/steamapps/common/SteamLinuxRuntime_soldier/run"), "--" ]
          else:
            
            steamRuntimeBinArgs = [ os.path.expanduser("~/.steam/root/steamapps/common/SteamLinuxRuntime_soldier/run"), "--" ]

    #Get GOG game's installed location
    if gametype != "epic":

      #Path to installed games via gog's installed.json file
      #goginstalledpath = os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"

      with open(configpath.goginstalledpath, encoding='utf-8') as l:
        goginstalled = json.load(l)

      goginstalledkeyarray = list(goginstalled['installed'])

      #Get install location
      gogGameLocation = None
      for game in goginstalledkeyarray:

        if appname == game['appName']:

          gogGameLocation = f"\"{game['install_path']}\""
          break
      if not gogGameLocation:
        raise Exception(f"Game {appname} not found in {configpath.goginstalledpath}")

    binaryLaunchArgs = [binary, "launch", appname] if gametype == "epic" else [binary, "launch", gogGameLocation, appname] 

    # Append the common arguments for all launchers to the baseArgs
    baseArgs = wrapperArgs + binaryLaunchArgs + targetExeArgs + offlineModeArgs
    #ADD IF-ELSE FOR GOG(LINUX OR WIN) AND EPIC
    if gametype == "epic" or gametype == "gog-win":


      #winePrefix
      winePrefix = f'\"{gameSettings["winePrefix"]}\"'

      #wineVersion (IMPACTS LAUNCH COMMAND)

      #wine bin & name 
      try:
        wineVersion_bin = gameSettings["wineVersion"]["bin"]
        wineVersion_name = gameSettings["wineVersion"]["name"]
        wineVersion_type = gameSettings["wineVersion"]["type"]
      except:
        logging.warning("No wineVersion key found. Defaulting wine version to the one used in Heroic's global settings...")
        #Use default wine version used in global settings 
        with open(configpath.heroicconfigpath, encoding='utf-8') as p:
            heroicconfig = json.load(p)

        wineVersion_bin = heroicconfig["defaultSettings"]["wineVersion"]["bin"]
        wineVersion_name = heroicconfig["defaultSettings"]["wineVersion"]["name"]
        wineVersion_type = heroicconfig["defaultSettings"]["wineVersion"]["type"]

      #enableEsync
      if gameSettings.get("enableEsync") and wineVersion_type == "wine":
          environment["WINEESYNC"] = "1"
      elif not gameSettings.get("enableEsync") and wineVersion_type == "proton":
          environment["PROTON_NO_ESYNC"] = "1"

      #enableFsync
      if gameSettings.get("enableFsync") and wineVersion_type == "wine":
          environment["WINEFSYNC"] = "1"
      elif not gameSettings.get("enableFsync") and wineVersion_type == "proton":
          environment["PROTON_NO_FSYNC"] = "1"

      if wineVersion_type == "wine":

        binArgs = ["--wine", wineVersion_bin]
        winePrefixArgs = ['--wine-prefix', winePrefix]

        #preferSystemLibs (custom wine libraries)
        if (gameSettings.get("preferSystemLibs") == False and wineVersion_type == "wine"):
            # https://github.com/ValveSoftware/Proton/blob/4221d9ef07cc38209ff93dbbbca9473581a38255/proton#L1091-L1093
            if (not os.environ.get("ORIG_LD_LIBRARY_PATH")):
                environment["ORIG_LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH") if os.environ.get("LD_LIBRARY_PATH") else ''
            
            if gameSettings["wineVersion"].get("lib") and gameSettings["wineVersion"].get("lib32"):
                wineVersion_lib = gameSettings["wineVersion"]["lib"]
                wineVersion_lib32 = gameSettings["wineVersion"]["lib32"]
                environment["LD_LIBRARY_PATH"] = f"{wineVersion_lib}:{wineVersion_lib32}"
                if os.environ.get("LD_LIBARY_PATH"):
                    environment["LD_LIBRARY_PATH"] = environment["LD_LIBRARY_PATH"].append(f":{os.environ.get('LD_LIBARY_PATH')}")

                #gstreamer path
                gstp_path_lib = os.path.join(wineVersion_lib, 'gstreamer-1.0')
                gstp_path_lib32 = os.path.join(wineVersion_lib32, 'gstreamer-1.0')
                environment["GST_PLUGIN_SYSTEM_PATH_1_0"] = f"{gstp_path_lib}:{gstp_path_lib32}"

                #winedll path
                winedll_path_lib = os.path.join(wineVersion_lib, 'wine')
                winedll_path_lib32 = os.path.join(wineVersion_lib32, 'wine')
                environment["WINEDLLPATH"] = f"{winedll_path_lib}:{winedll_path_lib32}"
            else:
                logging.warning(f"Could not find lib and lib32 for {wineVersion_name}")


        if gametype == "epic":

          arguments = baseArgs + languageArgs + winePrefixArgs + binArgs + launcherArgs

        elif gametype == "gog-win":#Windows GOG

          arguments = baseArgs + winePrefixArgs + binArgs + ["--os", "windows"] + launcherArgs
      elif wineVersion_type == "proton":
        if configpath.is_flatpak == False:
          environment["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = os.path.join(os.path.expanduser("~"), ".steam/steam")
        else:
           environment["STEAM_COMPAT_CLIENT_INSTALL_PATH"] = os.path.join(os.path.expanduser("~"), ".var/app/com.heroicgameslauncher.hgl/.steam/steam")
        
        environment["STEAM_COMPAT_DATA_PATH"] = winePrefix
        #Wrap Proton path (bin) in quotes to avoid errors due to spaces in the path
        wineVersion_bin = f"\'{wineVersion_bin}\'"

        #Check if Steam Soldier runtime is enabled
        if steam_runtime_win:
          binArgs = ['--no-wine', '--wrapper "'] + steamRuntimeBinArgs + [wineVersion_bin, 'waitforexitandrun"']
        else:
          binArgs = ['--no-wine', '--wrapper "', wineVersion_bin, 'run"']

        #Set Steam AppID
        environment['STEAM_COMPAT_APP_ID'] = "0"
        environment['SteamAppId'] = "0"
        if gametype == "epic":

          arguments = baseArgs + languageArgs + binArgs + launcherArgs
        elif gametype == "gog-win":#Windows GOG

          arguments = baseArgs + binArgs + ["--os", "windows"] + launcherArgs

    else:#LINUX GOG
      arguments = steamRuntimeBinArgs + baseArgs + ["--platform=linux"] + launcherArgs
  except Exception:

      logging.critical(traceback.format_exc())
      if not settings.args.silent:
        os.system('zenity --error --title="Process Failed" --text="\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
      sys.exit()

  #The entire launch command
  #print(environment)
  #print(arguments)

  #Return as list
  return [environment, arguments, cloudsync]
