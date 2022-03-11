import os, sys

#Zenity list box
contents = ('#!/bin/bash \n\n#Choose a game to be added to Steam \n\n' +
                'game=$(zenity --list --title="Add to Steam" --column="Game Name" --width=400 --height=400 ')


def createscript():

        global contents 

        contents = contents + ')\n./HeroicBashLauncher "$game" '

        with open("AddToSteam.sh", "w") as c:
                c.write(contents)
        os.system("chmod u+x AddToSteam.sh")


def addtoscript(simplified_gamename):
        
        global contents 

        contents = contents + simplified_gamename + " "


def addtosteam(simplified_gamename):

 try:

        finduserid = os.listdir(os.path.expanduser("~") + "/.steam/debian-installation/userdata/")

        #Finding a folder name with non-zero number
        for i in finduserid:
                if int(i) > 0:
                        userid = i

        
        #Read Steam shortcus file
        file=open(str(os.path.expanduser("~") + '/.steam/debian-installation/userdata/' + str(userid) + '/config/shortcuts.vdf'), 'rb')
        line=file.read()
        #print(line)
        file.close()
        



        #SYNTAX FOR ADDING NON-STEAM GAMES
        curr_dir = os.path.dirname(os.getcwd()) #till .../HeroicBashLauncher

        #Unicode Charaters
        nul = '\x00'
        soh = '\x01'
        stx = '\x02'
        bs = '\x08'

        #Keys
        srno = '\x00' + '\x00' # + number (starts from 0) self assigned by Steam
        #appid = stx + 'appid' + nul + nul + nul + nul + nul self assigned by Steam
        AppName = soh + 'AppName' + nul + simplified_gamename + '.sh' + nul
        Exe = soh + 'Exe' + nul + '"' + curr_dir + '/GameFiles/' + simplified_gamename + '.sh"' + nul
        StartDir = soh + 'StartDir' + nul + '"' + curr_dir + '/GameFiles/"' + nul
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
        print("Adding " + simplified_gamename + " to Steam")

        f=open(str(os.path.expanduser("~") + '/.steam/debian-installation/userdata/' + str(userid) + '/config/shortcuts.vdf'), 'wb')
        f.write(line[:len(line)-2] + entry.encode() + line[-2:])
        #print(line)
        file.close()
        
        os.system('zenity --info --title="Process Finished" --text="Game added. You can now restart Steam." --width=350')

        #Reading new
        #file=open(str(os.path.expanduser("~") + '/.steam/debian-installation/userdata/' + str(userid) + '/config/shortcuts.vdf'), 'rb')
        #line=file.read()
        #print(line)
        #file.close()
 except:
        os.system('zenity --error --title="Process Failed" --text="Failed to add game to Steam. Please check your console for the error and consider reporting it as an issue on Github." --width=400')
        sys.exit()

