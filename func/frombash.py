#Updates parameters of only individual games

import os,sys
from createlaunchfile import createlaunchfile

def frombash(gamename, appname, gamejson, gametype):

    createlaunchfile(gamename, appname, gamejson, gametype)

    print("Game parameters updated. Now launching game...")