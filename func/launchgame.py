#Updates parameters of only individual games

import os
from checkparameters import checkparameters
from createlaunchfile import createlaunchfile


def launch(gamename, appname, gamejson, gametype):
    
    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync
    launchcommand, offline_launchcommand, cloudsync = gamecommand[0], gamecommand[1], gamecommand[2]

    #Launch Fail Dialog
    fail_dialog= ('zenity --error --title="Error" --text="Failed to launch ' + gamename + '\n\nPlease check the game log under /logs/ for the error and consider reporting it as an issue on GitHub." --width=200')

    #START LAUNCHING THE GAME

    #Pre Cloud Save Sync
    if not cloudsync == "":
        os.system("printf '\nRunning pre-cloud save syncing....\n" + cloudsync[0] + "\n'")
        os.system(cloudsync[0])

    #Launch Game
    os.system("printf '\n\nRunning launch command for " + gamename + ":\n" + gamecommand[0] + "\n'")
    os.system('(' + launchcommand + '|| (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; ' + offline_launchcommand + ')) || (' + fail_dialog + ') ') 

    #Post Cloud Save Sync
    if not cloudsync == "":
        os.system("printf '\n\nRunning post-cloud save syncing....\n" + cloudsync[1] + "\n'")
        os.system(cloudsync[1])