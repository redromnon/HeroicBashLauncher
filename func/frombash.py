#Updates parameters of only individual games

import os,sys
from createlaunchfile import createlaunchfile

def frombash(gamename, appname, gamejson):

    #Moving one directory up
    os.chdir(os.path.dirname(os.getcwd()))

    #print(gamename + appname + gamejson)
    createlaunchfile(gamename, appname, gamejson)

    print("Game parameters updated. Now launching game...")