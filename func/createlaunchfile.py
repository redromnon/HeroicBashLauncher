#Creates the bash file

import os
from checkparameters import checkparameters
from gameName import getnameofgame
from steam import addtoscript

def createlaunchfile(gamename, appname, gamejson, gametype):

    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync, gametype

    #Generating game's name without special characters
    simplified_gamename = getnameofgame(gamename)

    #Creating the game file name
    #print(os.getcwd())
    gameFile = "GameFiles/" + simplified_gamename + ".sh"

    #Launch fail Dialog
    fail_dialog= ('zenity --error --title="Error" --text="Failed to launch games \n\nConsider posting the log as an issue" --width=200 --timeout=3')


    #Creating game file
    contents = ('#!/bin/bash \n\n' + '#Game Name = ' + gamename + ' (' + gametype.upper() + ') ' + 
                '\n\n' + '#App Name = ' + appname + '\n\n' + '#Overrides launch parameters\ncd .. && ./HeroicBashLauncher "' + 
                gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '" ' + 
                '\n\n' + gamecommand[2] + '\n\n(' + gamecommand[0] + 
                '|| (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; ' + gamecommand[1] + ')) || (' + fail_dialog + ')')
    
    with open(gameFile, "w") as g:
        g.write(contents)

    #Making the file executable
    os.system("chmod u+x " + gameFile)

    #Add to Steam script
    addtoscript(gamename)