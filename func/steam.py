import os, sys, traceback
from func.gameName import filegamename
from func.artwork import addartwork

#Zenity list box
contents = ('#!/bin/bash \n\n #Create log \n exec > AddToSteam.log 2>&1 \n\n#Choose a game to be added to Steam \n\n' +
                'game=$(zenity --list --title="Add to Steam" --checklist --column="Choose" --column="Game Name" --width=400 --height=400 ')


def createscript():

        global contents 

        contents = contents + ')\n./HeroicBashLauncher "$game" '

        with open("AddToSteam.sh", "w") as c:
                c.write(contents)
        os.system("chmod u+x AddToSteam.sh")

        print("AddtoSteam script successfully created")


def addtoscript(gamename):
        
        global contents 

        contents = contents + ' FALSE "' + gamename + '" '


def addtosteam(gamename):
        userdata_folder = os.path.join(os.path.expanduser("~"), '.steam' , 'steam', 'userdata')

        try:

                listuserid = os.listdir(userdata_folder)
    

                for userid in listuserid:

                        if userid != '0' and userid != 'ac': 
                                shortcutsvdfpath = os.path.join(userdata_folder, str(userid), 'config', 'shortcuts.vdf')
                                #Create shortcuts.vdf if doesn't exist
                                print("\n\n")
                                if os.path.isfile(shortcutsvdfpath) == False:
                                        os.makedirs(os.path.dirname(shortcutsvdfpath), exist_ok=True)
                                        file = open(str(shortcutsvdfpath), 'wb')
                                        file.write("\x00shortcuts\x00\x08\x08".encode())
                                        print("Created shortcuts.vdf in " + userid)
                                        file.close()
                                else:
                                        print("shortcuts.vdf already exists in " + userid)

                                #Read Steam shortcuts file
                                file = open(str(shortcutsvdfpath), 'rb')
                                line = file.read()
                                #print(line)
                                file.close()

                                #Generating game's filename
                                simplified_gamename = filegamename(gamename)
                                #print(simplified_gamename)


                                #SYNTAX FOR ADDING NON-STEAM GAMES
                                #till .../HeroicBashLauncher
                                if "GameFiles" in os.getcwd():
                                        curr_dir = os.getcwd() + "/"
                                else:
                                        curr_dir = os.getcwd() + "/GameFiles/"

                                #Unicode Charaters
                                nul = '\x00'
                                soh = '\x01'
                                stx = '\x02'
                                bs = '\x08'

                                #Keys
                                srno = '\x00' + '\x00' # + number (starts from 0) self assigned by Steam
                                #appid = stx + 'appid' + nul + nul + nul + nul + nul self assigned by Steam
                                AppName = soh + 'AppName' + nul + gamename + nul
                                Exe = soh + 'Exe' + nul + '"' + curr_dir + simplified_gamename + '.sh"' + nul
                                StartDir = soh + 'StartDir' + nul + '"' + curr_dir + '"' + nul
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


                                #Add game if not already added
                                if gamename in str(line.decode("utf-8", "ignore")): 

                                        print(gamename + " already added to Steam.")
                                else:

                                        
                                        #Writing to file
                                        print("Adding " + gamename + " to Steam")
                                        
                                        f=open(str(shortcutsvdfpath), 'wb')
                                        f.write(line[:len(line)-2] + entry.encode() + line[-2:])
                                        #print(line)
                                        file.close()  

                                #Add artwork
                                addartwork(gamename, '"' + curr_dir + simplified_gamename + '.sh"', userid, simplified_gamename)
        except Exception: 
                
                print(traceback.format_exc())

                if "deck" in os.path.expanduser("~"):
                        os.system('zenity --error --title="Process Failed" --text="Failed to add game to Steam. Please check the HeroicBashLauncher.log in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
                else:
                        os.system('zenity --error --title="Process Failed" --text="Failed to add game to Steam. Please check the AddToSteam.log in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
                sys.exit()
        

