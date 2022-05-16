#Creates the bash file

import os, json
import configpath
from checkparameters import checkparameters
from gameName import filegamename
from steam import addtoscript, addtosteam

def createlaunchfile(gamename, appname, gamejson, gametype):

    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync
    cloudsync = gamecommand[2]
    
    #Generating game's file name
    simplified_gamename = filegamename(gamename)

    #Creating the game file name
    if configpath.is_flatpak == False:

        if "GameFiles" in os.getcwd():#select parent dir
            executablepath = os.path.dirname(os.getcwd()) + '/HeroicBashLauncher' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"' 
            gameFilepath = os.getcwd() + "/" + simplified_gamename + ".sh"
        else:#launching from setup.sh
            executablepath = os.getcwd() + '/HeroicBashLauncher' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"'
            gameFilepath = os.getcwd() + "/GameFiles/" + simplified_gamename + ".sh"
    else:
        
        if "GameFiles" in os.getcwd():#select parent dir
            executablepath = 'flatpak run --command=' + os.path.dirname(os.getcwd()) + '/HeroicBashLauncher' + ' com.heroicgameslauncher.hgl' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"' 
            gameFilepath = os.getcwd() + "/" + simplified_gamename + ".sh"
        else:#launching from setup.sh
            executablepath = 'flatpak run --command=' + os.getcwd() + '/HeroicBashLauncher' ' com.heroicgameslauncher.hgl' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"' 
            gameFilepath = os.getcwd() + "/GameFiles/" + simplified_gamename + ".sh"

    #Launch Script Format
    launch_script = ("""
    #!/bin/bash 

    #Generate log
    exec > logs/{logname}.log 2>&1

    #Enable UTF-8 Encoding
    export LC_ALL=en_US.UTF-8

    #Game Name = {game_name} ({game_type}) 

    #App Name = {app_name}

    #Override launch parameters
    {executable_path}

    """).format(logname = simplified_gamename,game_name = gamename, game_type = gametype, app_name = appname, executable_path = executablepath)

    
    #Find game's exe file for tracking before post-game syncing (Epic)
    gameexe = ""

    with open(configpath.legendaryinstalledpath, encoding='utf-8') as l:
      installed = json.load(l) 

    #Games' AppNames stored in list 
    installedkeyarray = list(installed.keys())

    #Proceed to making launch files
    for i in installedkeyarray:

        if i == appname:
            gameexe = installed[i]['executable'].split('/')[-1]
            break

    
    #Epic Games Format
    epic_script = ("""

    #Launch game
    {cloudsyncdownload}

    ({launchcommand} || (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; {offline_launchcommand})) || (zenity --error --title="Error" --text="Failed to launch ' + {game_name} + '\n\nPlease check the game log under /logs/ for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    #Wait for game to launch
    sleep 6
    
    while [ 1 ]
    do

        SERVICE="{game_exe}"

        if pgrep -x "$SERVICE" >/dev/null
        then
            :
        else
            echo "$SERVICE stopped"
            {cloudsyncupload}
            exit
            # uncomment to start nginx if stopped
            # systemctl start nginx
            # mail  
        fi

        sleep 3
    done

    """).format(launchcommand = gamecommand[0], offline_launchcommand = gamecommand[1], 
                cloudsyncdownload = cloudsync[0], cloudsyncupload = cloudsync[1], game_exe = gameexe, game_name = gamename)

    
    #GOG format (without cloud sync check)
    gog_script = ("""

    #Launch game
    ({launchcommand} || (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; {offline_launchcommand})) || (zenity --error --title="Error" --text="Failed to launch ' + {game_name} + '\n\nPlease check the game log under /logs/ for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    """).format(launchcommand = gamecommand[0], offline_launchcommand = gamecommand[1], game_name = gamename) 

    
    #Create final launch script depending on gametype
    if gametype == "epic":
        final_launch_script = launch_script + epic_script
    else:
        final_launch_script = launch_script + gog_script
    
    
    #Write to file
    with open(gameFilepath, "w") as f:
            f.write(final_launch_script)
    #print(launch_script)
    
    
    #If system is Steam Deck, add to Steam right away or add to Steam script
    if "deck" in os.path.expanduser("~"):
        addtosteam(gamename)
    else:
        addtoscript(gamename)