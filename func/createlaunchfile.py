#Creates the launch script and additional flatpak launch script for launching games

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

    #Set file paths
    if "GameFiles" in os.getcwd():#select parent dir
        executablepath = os.path.dirname(os.getcwd()) + '/HeroicBashLauncher' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"' 
        gameFilepath = os.getcwd() + "/" + simplified_gamename + ".sh"
        flatpakgamescriptpath = os.getcwd() + "/launchflatpakgame.sh"
    else:#launching from setup.sh
        executablepath = os.getcwd() + '/HeroicBashLauncher' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"'
        gameFilepath = os.getcwd() + "/GameFiles/" + simplified_gamename + ".sh"
        flatpakgamescriptpath = os.getcwd() + "/GameFiles/launchflatpakgame.sh"
    
    if configpath.is_flatpak == False:
        launchflatpakgame = ''
    else:
        launchflatpakgame = 'flatpak run --command=./launchflatpakgame.sh com.heroicgameslauncher.hgl' 

    ####################################################################################################################
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

    {launch_game_in_flatpak}

    """).format(logname = simplified_gamename,game_name = gamename, game_type = gametype, app_name = appname, 
                executable_path = executablepath, launch_game_in_flatpak = launchflatpakgame)

    
    #Flatpak Game Script Format
    launch_flatpak_script = ("""
    #!/bin/bash

    #Currently created launch script for {game_name} ({app_name}) ({game_type})
    #Launches from {gamelaunchscript}.sh


    """).format(game_name = gamename, game_type = gametype, app_name = appname, gamelaunchscript = simplified_gamename)


    
    #Epic Games Format (Track wineserver before running post-game sync)
    epic_script = ("""

    #Launch game
    {cloudsyncdownload}

    ({launchcommand} || (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; {offline_launchcommand})) || (zenity --error --title="Error" --text="Failed to launch {game_name}\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    #Wait for game to launch
    sleep 10
    
    while [ 1 ]
    do

        checkwine="wineserver"

        if pgrep -x "$checkwine" >/dev/null
        then
            :
        else
            echo "$checkwine stopped"
            echo "{game_name} stopped"
            {cloudsyncupload}
            exit 
        fi

        sleep 3
    done

    """).format(launchcommand = gamecommand[0], offline_launchcommand = gamecommand[1], 
                cloudsyncdownload = cloudsync[0], cloudsyncupload = cloudsync[1], game_name = gamename)

    
    #GOG format (without cloud sync check)
    gog_script = ("""

    #Launch game
    ({launchcommand} || (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; {offline_launchcommand})) || (zenity --error --title="Error" --text="Failed to launch ' + {game_name} + '\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    """).format(launchcommand = gamecommand[0], offline_launchcommand = gamecommand[1], game_name = gamename) 

    ####################################################################################################################
    #Create final launch script depending on gametype
    if configpath.is_flatpak == False:
        if gametype == "epic":
            final_launch_script = launch_script + epic_script
        else:
            final_launch_script = launch_script + gog_script
    else:
        
        final_launch_script = launch_script
        
        if gametype == "epic":
            flatpak_launch_script = launch_flatpak_script + epic_script 
        else:
            flatpak_launch_script = launch_flatpak_script + gog_script 
    
    
    #Write to file
    with open(gameFilepath, "w") as f:
            f.write(final_launch_script)
    os.system("chmod u+x " + gameFilepath)

    if configpath.is_flatpak == True:

        with open(flatpakgamescriptpath, "w") as f:
            f.write(flatpak_launch_script)
        os.system("chmod u+x " + flatpakgamescriptpath)
    
    
    #If system is Steam Deck, add to Steam right away or add to Steam script
    if "deck" in os.path.expanduser("~"):
        addtosteam(gamename)
    else:
        addtoscript(gamename)