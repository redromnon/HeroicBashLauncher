import os, sys
from gameName import filegamename
import configpath 

#Zenity list box
contents = ('#!/bin/bash \n\n#Choose a game to be added to Steam \n\n' +
                'game=$(zenity --list --title="Add to Steam" --column="Game Name" --width=400 --height=400 ')


def createscript():

        global contents 

 
        #Check if Flatpak
        if configpath.is_flatpak == True:

                contents = contents + ')\ncd GameFiles && ./HeroicBashLauncher "$game" '

                #Move up directory outside GameFiles
                os.chdir(os.path.dirname(os.getcwd()))
        else:

                contents = contents + ')\n./HeroicBashLauncher "$game" '


        with open("AddToSteam.sh", "w") as c:
                c.write(contents)
        os.system("chmod u+x AddToSteam.sh")


def addtoscript(gamename):
        
        global contents 

        contents = contents + '"' + gamename + '" '


def addtosteam(gamename):

 try:

        finduserid = os.listdir(os.path.expanduser("~") + "/.steam/steam/userdata/")

        #Finding a folder name with non-zero number
        for i in finduserid:
                if int(i) > 0:
                        userid = i
                        if (os.path.exists(os.path.expanduser("~") + '/.steam/steam/userdata/' + str(userid) + '/config/shortcuts.vdf')):
                                print("Selecting Steam userid - " + userid)
                                break
                        else:
                                pass
        
        #Read Steam shortcus file
        file=open(str(os.path.expanduser("~") + '/.steam/steam/userdata/' + str(userid) + '/config/shortcuts.vdf'), 'rb')
        line=file.read()
        #print(line)
        file.close()
        

        #Generating game's filename
        simplified_gamename = filegamename(gamename)
        print(simplified_gamename)

        #GameFiles dir if non-Flatpak
        if configpath.is_flatpak == True:
                GameFiles = "/"
        else:
                GameFiles = "/GameFiles/"

        #SYNTAX FOR ADDING NON-STEAM GAMES
        curr_dir = os.getcwd() #till .../HeroicBashLauncher

        #Unicode Charaters
        nul = '\x00'
        soh = '\x01'
        stx = '\x02'
        bs = '\x08'

        #Keys
        srno = '\x00' + '\x00' # + number (starts from 0) self assigned by Steam
        #appid = stx + 'appid' + nul + nul + nul + nul + nul self assigned by Steam
        AppName = soh + 'AppName' + nul + gamename + nul
        Exe = soh + 'Exe' + nul + '"' + curr_dir + GameFiles + simplified_gamename + '.sh"' + nul
        StartDir = soh + 'StartDir' + nul + '"' + curr_dir + GameFiles + '"' + nul
        icon = soh + 'icon' + nul + nul
        ShortcutPath = soh + 'ShortcutPath' + nul + nul
        LaunchOptions = soh + 'LaunchOptions' + nul + nul
        IsHidden = stx + 'IsHidden' + nul + nul + nul + nul + nul
        AllowDesktopConfig = stx + 'AllowDesktopConfig' + nul + soh  + nul + nul + nul
        AllowOverlay = stx + 'AllowOverlay' + nul + soh  + nul + nul + nul
        OpenVR = stx + 'OpenVR' + nul + nul + nul + nul + nul
        Devkit = stx + 'Devkit' + nul + nul + nul + nul + nul
        DevkitGameID = soh + 'DevkitGameID' + nul + nul
        DevkitOverrideAppID = stx + 'DevkitOverrideAppID' + nul + nul + nul + nul + nul
        LastPlayTime = stx + 'LastPlayTime' + nul + nul + nul + nul + nul
        tags = nul + 'tags' + nul
        end = bs + bs

        #Entry
        entry = srno + AppName + Exe + StartDir + icon + ShortcutPath + LaunchOptions + IsHidden + AllowDesktopConfig + AllowOverlay + \
                OpenVR + Devkit + DevkitGameID + DevkitOverrideAppID + LastPlayTime + tags + end
        





        #Writing to file
        print("Adding " + gamename + " to Steam")

        f=open(str(os.path.expanduser("~") + '/.steam/steam/userdata/' + str(userid) + '/config/shortcuts.vdf'), 'wb')
        f.write(line[:len(line)-2] + entry.encode() + line[-2:])
        #print(line)
        file.close()
        
        os.system('zenity --info --title="Process Finished" --text="Game added. You can now restart Steam." --width=350')
 except:
        os.system('zenity --error --title="Process Failed" --text="Failed to add game to Steam. Please check your console for the error and consider reporting it as an issue on Github." --width=400')
        sys.exit()
        

