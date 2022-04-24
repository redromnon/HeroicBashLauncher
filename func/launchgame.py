#Updates parameters of only individual games

import os
from checkparameters import checkparameters
from createlaunchfile import createlaunchfile


def launch(gamename, appname, gamejson, gametype):
    
    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync
    launchcommand, offline_launchcommand, cloudsync = gamecommand[0], gamecommand[1], gamecommand[2]

    #Launch Fail Dialog
    fail_dialog= ('zenity --error --title="Error" --text="Failed to launch games \n\nConsider posting the log as an issue" --width=200 --timeout=3')

    #START LAUNCHING THE GAME

    #Pre Cloud Save Sync
    if not cloudsync == "":
        os.system("printf '\nRunning pre-cloud save syncing....\n'")
        os.system(cloudsync)

    #Launch Game
    os.system("printf '\n\nRunning launch command for " + gamename + ":\n" + gamecommand[0] + "\n'")
    os.system('(' + launchcommand + '|| (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; ' + offline_launchcommand + ')) || (' + fail_dialog + ') ') 

    #Post Cloud Save Sync
    if not cloudsync == "":
        os.system("printf '\n\nRunning post-cloud save syncing....\n'")
        os.system(cloudsync)