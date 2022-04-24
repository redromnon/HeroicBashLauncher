#Creates the bash file

import os
import configpath
from checkparameters import checkparameters
from gameName import filegamename
from steam import addtoscript, addtosteam
from flatpak import getflatpakpath

def createlaunchfile(gamename, appname, gamejson, gametype):

    # Check/Update parameters
    #gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync

    #Generating game's file name
    simplified_gamename = filegamename(gamename)

    #Creating the game file name
    #print(os.getcwd())
    gameFile = "GameFiles/" + simplified_gamename + ".sh"

    #Launch fail Dialog
    fail_dialog= ('zenity --error --title="Error" --text="Failed to launch games \n\nConsider posting the log as an issue" --width=200 --timeout=3')

    #Launch script contents
    if configpath.is_flatpak == False:
        contents = ('#!/bin/bash \n\n' + '#Generate log\n' + 'exec > logs/' + simplified_gamename + '.log 2>&1' + 
                '\n\n' + '#Game Name = ' + gamename + ' (' + gametype.upper() + ') ' + 
                '\n\n' + '#App Name = ' + appname + '\n\n' + '#Overrides launch parameters\ncd .. && ./HeroicBashLauncher "' + 
                gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '" ')
    
        with open(gameFile, "w") as g:
            g.write(contents)

        #Making the file executable
        os.system("chmod u+x " + gameFile)
    else:

        #Entire path to GameFiles dir
        fullpath = getflatpakpath(os.path.abspath(os.getcwd()))
        
        contents = ('#!/bin/bash\n\n' + '#Generate log\n' + 'exec > logs/' + simplified_gamename + '.log 2>&1' + 
                '\n\n' + '#Game Name = ' + gamename + ' (' + gametype.upper() + ') ' + 
                '\n\n' + '#App Name = ' + appname + '\n\n' + '#Override launch parameters and launch game\n' + 
                'flatpak run --command=./' + 'HeroicBashLauncher' + ' com.heroicgameslauncher.hgl "' +
                gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '" ' + '"flatpak"' + 
                ' || ' + 'flatpak run --command=./' + fullpath + '/HeroicBashLauncher' + ' com.heroicgameslauncher.hgl "' +
                gamename + '" "' + appname + '" "' + gamejson + '" "' + gametype + '" ' + '"flatpak"')
        
        with open(simplified_gamename + ".sh", "w") as g:
            g.write(contents)

        #Making the file executable
        os.system("chmod u+x " + simplified_gamename + ".sh")


    #If system is Steam Deck, add to Steam right away or add to Steam script
    if "deck" in os.path.expanduser("~"):
        addtosteam(gamename)
    else:
        addtoscript(gamename)