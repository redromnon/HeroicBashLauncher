#DISCLAIMER - The logic of the code on Line 18 has been taken from SteamGridDB (https://github.com/SteamGridDB/steamgriddb-manager) [MIT License].   


import os, binascii, json
import configpath
from gameName import rspchar

def addartwork(appname, exe, userid, simplified_gamename):
    

    #As Steam does not store AppIDs of Non-Steam games in any config file, this makes it difficult to add artwork without knowing the AppID.
    #One way is to add the game, let Steam assign the AppID and then try to find the AppID using regex.
    #Fortunately, SteamGridDB (MIT License) has found a simple and efficient solution to calculate the AppID. 
    
    #ALL CREDIT GOES TO THE STEAMGRIDDB DEVS FOR THIS IMPLEMENTATION (Line 18).
    #Here's how the it's explained in their source code - 
        #To create a grid image we must compute the Steam ID, which is just crc32(target + label) + "02000000", using IEEE standard polynomials.
    appid = binascii.crc32(str.encode(exe + appname)) | 0x80000000
    print("Steam AppID for " + appname + " is " + str(appid))

    #Check if appid exists in the image file name 
    check_flag = 0

    #Path to Steam grid folder
    artwork_path = os.path.expanduser("~") + '/.steam/steam/userdata/' + str(userid) + '/config/grid'

    for i in os.listdir(artwork_path):
           
        if str(appid) in i:
            print("Artwork already exists")
            check_flag = 1
            break

    if check_flag == 0:
        print("Adding Artwork...")

        #GameFiles dir if non-Flatpak
        if configpath.is_flatpak == True:
            GameFiles = ""
        else:
            GameFiles = "GameFiles/"

        #Reading from file
        openscript = open(GameFiles + simplified_gamename + ".sh", 'r')
        readscript = openscript.read()
        openscript.close()

        #Check if game is Epic or GOG
        if "EPIC" in readscript:
            
            #print("Epic")

            with open(configpath.heroiclibrarypath, encoding='utf-8') as l:
                heroicinstalled = json.load(l)

            for i in heroicinstalled['library']:

                gamename = rspchar(i['title'])
                
                if appname == gamename:
                    print("Yes")
                    image_url = i['art_square']
                    print(image_url)

            #Download image to Steam grid and rename as appid
            os.system('wget -P ' + artwork_path + ' ' + image_url)
            #wget.download(image_url, out = artwork_path)
            os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + str(appid) + 'p.jpg')

        elif "GOG" in readscript:
            
            #print("GOG")

            with open(configpath.goglibrarypath, encoding='utf-8') as l:
                heroicinstalled = json.load(l)

            for i in heroicinstalled['games']:

                gamename = rspchar(i['title'])
                
                if appname == gamename:
                    print("Yes")
                    image_url = i['art_square']
                    print(image_url)

            #Download image to Steam grid, extract image name and rename as appid (URL GOG format different than Epic)
            #wget.download(image_url, out = artwork_path)
            os.system('wget -P ' + artwork_path + ' ' + image_url)
            extract_image_url = image_url.split("/")[-1]
            os.rename(artwork_path + '/' + extract_image_url.split("?")[0], artwork_path + '/' + str(appid) + 'p.jpg')
