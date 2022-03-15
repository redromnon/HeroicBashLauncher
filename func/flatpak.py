import os
from checkparameters import checkparameters


#SET PATH TO GAME'S LAUNCH SCRIPT IN FLATPAK
def getflatpakpath(flatpakpath):
   
    #Count no. of "/"
    count = 0
    c = 0

    for i in flatpakpath:
        if count == 3:
            c = flatpakpath.index(i)
            break

        if i == "/":
            count = count + 1
    
    #print(count)

    return flatpakpath[c:]


#DIRECTLY LAUNCH FLATPAK GAME
def launchflatpakgame(gamename, appname, gamejson, gametype, flatpak):

    # Check/Update parameters
    gamecommand = checkparameters(appname, gamejson, gametype) # returns launchcommand, offline_launchcommand, cloudsync, gametype

    #Launch fail Dialog
    fail_dialog= ('zenity --error --title="Error" --text="Failed to launch games \n\nConsider posting the log as an issue" --width=200 --timeout=3')

    #Show game launch
    print("Launch command:\n" + gamecommand[0])

    #Launch game
    os.system(gamecommand[2] + '\n\n(' + gamecommand[0] + 
                '|| (echo "---CANNOT CONNECT TO NETWORK. RUNNING IN OFFLINE MODE---" ; ' + gamecommand[1] + ')) || (' + fail_dialog + ')')
          