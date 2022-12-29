#Creates the launch script and additional flatpak launch script for launching games

import os, json, logging, sys
from func import configpath
from func.checkparameters import checkparameters
from func.gameName import filegamename
from func.settings import args

def createlaunchfile(gamename, appname, gamejson, gametype):

    #Check if the game is launched at least once in Heroic
    if os.path.isfile(configpath.timestamppath):
        with open(configpath.timestamppath, encoding='utf-8') as p:
            gametimelist = json.load(p)
    else:
        logging.error("timestamp.json not found. Looks like you haven't launched any game from Heroic at all. Please consider doing so.")
        if not args.silent:
            os.system('zenity --error --title="Process Failed" --text="timestamp.json not found. Looks like you have not launched any game from Heroic at all. Please consider doing so." --width=200 --timeout=10')
        sys.exit()


    if appname not in gametimelist.keys():
        new_game_message = 'zenity --warning --title="Process Stopped" --text="Looks like ' + gamename + ' is newly installed\n\nPlease run the game directly from Heroic for the initial setup and verify if it works." --width=200 --timeout=8; exit'
    else:
        new_game_message = ''
    
    # Check/Update parameters
    environment, gameArguments, cloudsync = checkparameters(appname, gamejson, gametype) # returns launchcommand, cloudsync
    environmentString = " ".join([f"{k}=\"{v}\"" for k, v in environment.items()])
    gameString = " ".join(gameArguments)
    
    #Generating game's file name
    simplified_gamename = filegamename(gamename)

    #Set file paths
    if "GameFiles" in os.getcwd():#select parent dir
        executablepath = os.path.dirname(os.getcwd()) + '/HeroicBashLauncher --update' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"' 
        gameFilepath = os.getcwd() + "/" + simplified_gamename + ".sh"
        flatpakgamescriptpath = os.getcwd() + "/launchflatpakgame.sh"
    else:#launching from setup.sh
        executablepath = os.getcwd() + '/HeroicBashLauncher --update' + ' "' + gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '"'
        gameFilepath = os.getcwd() + "/GameFiles/" + simplified_gamename + ".sh"
        flatpakgamescriptpath = os.getcwd() + "/GameFiles/launchflatpakgame.sh"
    
    #Launch commands for flatpak
    if configpath.is_flatpak == False:
        launchflatpakgame = ''
        showlaunchcommand = ''
    else:
        launchflatpakgame = 'flatpak run --command=./launchflatpakgame.sh com.heroicgameslauncher.hgl' 
        showlaunchcommand = '#Launch Command\n    #' + gameString #Left space for alignment

    ####################################################################################################################
    #Launch Script Format
    launch_script = f"""#!/bin/bash 

    #Generate log
    exec > logs/{simplified_gamename}.log 2>&1

    #Enable UTF-8 Encoding
    export LC_ALL=en_US.UTF-8

    #Game Name = {gamename} ({gametype}) 

    #App Name = {appname}

    #Override launch parameters
    {executablepath}

    {new_game_message}

    {launchflatpakgame}

    {showlaunchcommand}
    """

    
    #Flatpak Game Script Format
    launch_flatpak_script = (f"""#!/bin/bash

    #Currently created launch script for {gamename} ({appname}) ({gametype})
    #Launches from {simplified_gamename}.sh
    """)

    #Epic Games Format (Track wineserver before running post-game sync)
    epic_script = f"""
    #Launch game
    {cloudsync}
    {environmentString} {gameString}

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
            echo "{gamename} stopped"
            {cloudsync}
            exit 
        fi

        sleep 3
    done
    """
    #GOG format (without cloud sync check)
    gog_script = f"""

    #Launch game
    {environmentString} {gameString}

    """

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

    if configpath.is_flatpak:

        with open(flatpakgamescriptpath, "w") as f:
            f.write(flatpak_launch_script)
        os.system("chmod u+x " + flatpakgamescriptpath)
        