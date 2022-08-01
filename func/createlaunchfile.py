#Creates the launch script and additional flatpak launch script for launching games

import os
from func import configpath
from func.gameName import filegamename

def createlaunchfile(gamename, appname, gametype):
    
    #Generating game's file name
    simplified_gamename = filegamename(gamename)

    #Set file paths
    if "GameFiles" in os.getcwd():#select parent dir
        gameFilepath = os.getcwd() + "/" + simplified_gamename + ".sh"
    else:#launching from setup.sh
        gameFilepath = os.getcwd() + "/GameFiles/" + simplified_gamename + ".sh"

    #Launch game command
    if configpath.is_flatpak:
        launch_command = 'flatpak run com.heroicgameslauncher.hgl --no-gui --no-sandbox "heroic://launch/' + appname + '"'
    else:
        launch_command = '/opt/Heroic/heroic --no-gui --no-sandbox "heroic://launch/' + appname + '"'
    
    '''
    #Launch commands for flatpak
    if configpath.is_flatpak == False:
        launchflatpakgame = ''
        showlaunchcommand = ''
    else:
        launchflatpakgame = 'flatpak run --command=./launchflatpakgame.sh com.heroicgameslauncher.hgl' 
        showlaunchcommand = '#Launch Command\n    #' + gamecommand[0]#Left space for alignment
    '''

    ####################################################################################################################
    #Launch Script Format
    launch_script = ("""#!/bin/bash 

    #Game Name = {game_name} ({game_type}) 

    #App Name = {app_name}

    #Launch Game
    {launch_game_command}

    """).format(logname = simplified_gamename, game_name = gamename, game_type = gametype, app_name = appname,
                launch_game_command = launch_command)
    
    
    #Write to file
    with open(gameFilepath, "w") as f:
            f.write(launch_script)
    os.system("chmod u+x " + gameFilepath)
        