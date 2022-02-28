#Creates the bash file

import os
from checkparameters import checkparameters
from gameName import getnameofgame

def createlaunchfile(gamename, appname, gamejson):

    # Check/Update parameters
    heroiccommand = checkparameters(appname, gamejson) # returns launchcommand, offline_launchcommand, cloudsync

    #Generating game's name without special characters
    simplified_gamename = getnameofgame(gamename)

    #Creating the game file name
    #print(os.getcwd())
    gameFile = "GameFiles/" + simplified_gamename + ".sh"

    #Offline Dialog
    offline_dialog= "Cannot connect to Epic servers. Running game in offline mode."

    #Creating game file
    contents = ('#!/bin/bash \n\n' + '#Game Name = ' + gamename + '\n\n' + '#App Name (Legendary) = ' + appname + 
                '\n\n' + '#Overrides launch parameters\ncd .. && ./HeroicBashLauncher "' + gamename + '" "' + appname + '" "' + gamejson + '" ' +
                '\n\n' + heroiccommand[2] + '\n\n' + heroiccommand[0] + '|| ( ' + offline_dialog + ' ; ' + heroiccommand[1] + ')')
    
    with open(gameFile, "w") as g:
        g.write(contents)

    #Making the file executable
    os.system("chmod u+x " + gameFile)
