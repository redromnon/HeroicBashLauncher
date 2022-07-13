#Adding launch scripts to Steam

import os, sys, traceback, binascii, logging
from func.gameName import filegamename
from func.artwork import addartwork
from func import settings

#Zenity list box
contents = ('#!/bin/bash \n\n#Choose a game to be added to Steam \n\n' +
                'game=$(zenity --list --title="Add to Steam" --checklist --column="Choose" --column="Game Name" --width=400 --height=400 ')


def createscript():

        global contents 

        contents = contents + ')\n./HeroicBashLauncher "$game" '

        with open("AddToSteam.sh", "w") as c:
                c.write(contents)
        os.system("chmod u+x AddToSteam.sh")

        logging.info("AddtoSteam script successfully created")


def addtoscript(gamename):
        
        global contents 

        contents = contents + ' FALSE "' + gamename + '" '


def calculateappid(appname, exepath):

#As Steam does not store AppIDs of Non-Steam games in any config file, this makes it difficult to add artwork without knowing the AppID.
#One way is to add the game, let Steam assign the AppID and then try to find the AppID using regex.
#Fortunately, steamgrid (https://github.com/boppreh/steamgrid) [MIT License] has found a simple and efficient solution to calculate the AppID. 
    
#ALL CREDIT GOES TO THE STEAMGRID DEVS FOR THIS IMPLEMENTATION.
#Here's how the it's explained in their source code (games.go) - 
#To create a grid image we must compute the Steam ID, which is just crc32(target + label) + "02000000", using IEEE standard polynomials.
        
        appid = binascii.crc32(str.encode(exepath + appname)) | 0x80000000

        return appid


def calculate_last_srno(line):

        start = -1
        no_entries = True

        #Begin iterating from the end of the file
        while start > -len(line):

                if "appid".encode() in line[start:]:
                        no_entries = False
                        #print("Found appid")
                        break

                start = start - 1

        #If no entries found, set srno as 0 otherwise increment last srno
        if no_entries == True:
                return '0'
        else:
                if '\x00'.encode() not in line[start-5:start-2]:#Should be three digits like 100,101,...999
                        num = str(line[start-5:start-2].decode())
                elif '\x00'.encode() not in line[start-4:start-2]:#Should be two digits like 10,11,...99
                        num = str(line[start-4:start-2].decode())
                else:#Should be one digit like 0,1,...9
                        num = str(line[start-3:start-2].decode())

                
                num = int(num) + 1
                return str(num)



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
                                        logging.info("Created shortcuts.vdf in " + userid)
                                        file.close()
                                else:
                                        logging.warning("shortcuts.vdf already exists in " + userid)

                                #Read Steam shortcuts file
                                file = open(str(shortcutsvdfpath), 'rb')
                                line = file.read()
                                #print("Printing vdf file = \n", line, "\n\n")
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

                                #Calculate appid and last srno
                                exepath = '"' + curr_dir + simplified_gamename + '.sh"'
                                gameappid = calculateappid(gamename, exepath)

                                last_srno = calculate_last_srno(line)
                                
                                #Keys
                                srno = nul + last_srno + nul
                                appid = stx + 'appid' + nul + nul + nul + nul + nul
                                AppName = soh + 'AppName' + nul + gamename + nul
                                Exe = soh + 'Exe' + nul + exepath + nul
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
                                entry = srno + appid + AppName + Exe + StartDir + icon + ShortcutPath + LaunchOptions + IsHidden + AllowDesktopConfig + AllowOverlay + \
                                        OpenVR + Devkit + DevkitGameID + DevkitOverrideAppID + LastPlayTime + tags + end


                                #Add game if not already added
                                if gamename in str(line.decode("utf-8", "ignore")): 

                                        logging.warning(gamename + " already added to Steam.")
                                else:

                                        
                                        #Writing to file
                                        logging.info("Adding " + gamename + " to Steam")
                                        
                                        f=open(str(shortcutsvdfpath), 'wb')
                                        f.write(line[:len(line)-2] + entry.encode() + line[-2:])
                                        #print(line)
                                        file.close()  

                                        #Add artwork
                                        if settings.enable_artwork:
                                                addartwork(gamename, gameappid, userid, simplified_gamename)
        except Exception: 
                
                logging.critical(traceback.format_exc())

                if "deck" in os.path.expanduser("~"):
                        os.system('zenity --error --title="Process Failed" --text="Failed to add game to Steam. Please check the HeroicBashLauncher.log in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
                else:
                        os.system('zenity --error --title="Process Failed" --text="Failed to add game to Steam. Please check the AddToSteam.log in the HeroicBashLauncher folder for the error and consider reporting it as an issue on GitHub." --width=400')
                sys.exit()
        

