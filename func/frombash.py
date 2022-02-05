#Updates parameters of only individual games

import os,sys
from createlaunchfile import createlaunchfile

#Take arguments
gamename = sys.argv[1]
appname = sys.argv[2]
gamejson = sys.argv[3]

#Moving one directory up
os.chdir(os.path.dirname(os.getcwd()))

#print(gamename + appname + gamejson)
createlaunchfile(gamename, appname, gamejson)

print("Game parameters updated. Now launching game...")