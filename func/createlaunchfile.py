#Creates the launch script and additional flatpak launch script for launching games

import os, json, logging, sys
from func import configpath
from func.checkparameters import checkparameters
from func.gameName import filegamename

def createlaunchfile(gamename, appname, gamejson, gametype):

    #Check if the game is launched at least once in Heroic
    if os.path.isfile(configpath.timestamppath):
        with open(configpath.timestamppath, encoding='utf-8') as p:
            gametimelist = json.load(p)
    else:
        logging.error("timestamp.json not found. Looks like you haven't launched any game from Heroic at all. Please consider doing so.")
        os.system('zenity --error --title="Process Failed" --text="timestamp.json not found. Looks like you have not launched any game from Heroic at all. Please consider doing so." --width=200 --timeout=10')
        sys.exit()


    if appname not in gametimelist.keys():
        new_game_message = 'zenity --warning --title="Process Stopped" --text="Looks like ' + gamename + ' is newly installed\n\nPlease run the game directly from Heroic for the initial setup and verify if it works." --width=200 --timeout=8; exit'
    else:
        new_game_message = ''
    
    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, cloudsync
    cloudsync = gamecommand[1]
    
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
        showlaunchcommand = '#Launch Command\n    #' + gamecommand[0]#Left space for alignment

    ####################################################################################################################
    #Launch Script Format
    launch_script = ("""#!/bin/bash 

    #Generate log
    exec > logs/{logname}.log 2>&1

    #Enable UTF-8 Encoding
    export LC_ALL=en_US.UTF-8

    #Game Name = {game_name} ({game_type}) 

    #App Name = {app_name}

    #Override launch parameters
    {executable_path}

    {new_game_zenity}

    {launch_game_in_flatpak}

    {show_launch_command}

    """).format(logname = simplified_gamename,game_name = gamename, game_type = gametype, app_name = appname, 
                executable_path = executablepath, launch_game_in_flatpak = launchflatpakgame, 
                new_game_zenity = new_game_message, show_launch_command = showlaunchcommand)

    
    #Flatpak Game Script Format
    launch_flatpak_script = ("""#!/bin/bash

    #Currently created launch script for {game_name} ({app_name}) ({game_type})
    #Launches from {gamelaunchscript}.sh


    """).format(game_name = gamename, game_type = gametype, app_name = appname, gamelaunchscript = simplified_gamename)


    
    #Epic Games Format (Track wineserver before running post-game sync)
    epic_script = ("""

    #Launch game
    {savesync}

    {launchcommand} || (zenity --error --title="Error" --text="Failed to launch {game_name}\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=200; exit)

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
            {savesync}
            exit 
        fi

        sleep 3
    done

    """).format(launchcommand = gamecommand[0], savesync = cloudsync, game_name = gamename)

    
    #GOG format (without cloud sync check)
    gog_script = ("""

    #Launch game
    {launchcommand} || (zenity --error --title="Error" --text="Failed to launch {game_name}\n\nPlease check the game log under GameFiles/logs/ in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=200; exit)

    """).format(launchcommand = gamecommand[0], game_name = gamename) 

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
        