#DISCLAIMER - The logic of the code on Line 18 has been taken from SteamGridDB (https://github.com/SteamGridDB/steamgriddb-manager) [MIT License].   


import os, json, wget, ssl, traceback, sys, logging
from func import configpath
from func.gameName import rspchar
from func import settings

def checkartworkexists(artwork_path, image):
    
    check_flag = 0

    for i in os.listdir(artwork_path):
           
        if i in image:
            check_flag = 1
            break

    if check_flag == 1:

        return True
    else:

        return False


def addartwork(appname, appid, userid, simplified_gamename):

    #Path to Steam grid folder
    artwork_path = os.path.expanduser("~") + '/.steam/steam/userdata/' + str(userid) + '/config/grid'


    #Artwork types
    logging.info("Steam AppID for " + appname + " is " + str(appid))
    coverart =  [str(appid) + 'p.jpg', str(appid) + 'p.png']
    backgroundart = [str(appid) + '_hero.jpg', str(appid) + '_hero.png']
    bigpictureart = [str(appid) + '.jpg', str(appid) + '.png']
    logoart = [str(appid) + '_logo.jpg', str(appid) + '_logo.png']


    #Check if the folder exists, create if not
    grid_exists = os.path.isdir(artwork_path)

    if not grid_exists:
        os.makedirs(artwork_path)
        logging.info("Created grid folder in ", artwork_path)

    

    try:

        logging.info("Checking Artwork...")

        if "GameFiles" in os.getcwd():
            GameFiles = os.getcwd() + "/"
        else:
            GameFiles = os.getcwd() + "/GameFiles/"

        #Reading from file
        openscript = open(GameFiles + simplified_gamename + ".sh", 'r')
        readscript = openscript.read()
        openscript.close()

        #Avoid SSL certificate error
        ssl._create_default_https_context = ssl._create_unverified_context

        #Check if game is Epic or GOG
        if "epic" in readscript:
            
            #print("Epic")

            with open(configpath.heroiclibrarypath, encoding='utf-8') as l:
                epicinstalled = json.load(l)

            for i in epicinstalled['library']:

                gamename = rspchar(i['title'])
                
                if appname == gamename:

                    #Cover Art
                    if checkartworkexists(artwork_path, coverart) == False:
                    
                        image_url = i['art_square']
                        logging.info("Downloading Cover Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + coverart[0])
                    else:
                        logging.info("Covert Art exists")

                    #Background Art
                    if checkartworkexists(artwork_path, backgroundart) == False:
                    
                        image_url = i['art_cover']
                        logging.info("Downloading Background Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + backgroundart[0])
                    else:
                        logging.info("Background Art exists")

                    #BigPicture Art
                    if checkartworkexists(artwork_path, bigpictureart) == False:
                    
                        image_url = i['art_cover']
                        logging.info("Downloading BigPicture Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + bigpictureart[0])
                    else:
                        logging.info("BigPicture Art exists")

                    #Logo Art
                    try:
                        if checkartworkexists(artwork_path, logoart) == False:
                        
                            if not i['art_logo'] == None:
                                image_url = i['art_logo']
                                logging.info("Downloading Logo Art from " + image_url)
                                wget.download(image_url, out = artwork_path)
                                os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + logoart[0])
                        else:
                            logging.info("Logo Art exists")
                    except:
                        logging.warning("Cannot find Logo Art for this game")
        elif "gog" in readscript:
            
            #print("GOG")

            with open(configpath.goglibrarypath, encoding='utf-8') as l:
                goginstalled = json.load(l)

            for i in goginstalled['games']:

                gamename = rspchar(i['title'])
                
                if appname == gamename:

                    #Cover Art
                    if checkartworkexists(artwork_path, coverart) == False:
                    
                        image_url = i['art_square']
                        logging.info("Downloading Cover Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        extract_image_url = image_url.split("/")[-1]
                        os.rename(artwork_path + '/' + extract_image_url.split("?")[0], artwork_path + '/' + coverart[0])
                    else:
                        logging.info("Covert Art exists")

                    #Background Art
                    if checkartworkexists(artwork_path, backgroundart) == False:
                    
                        image_url = i['art_cover']
                        logging.info("Downloading Background Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + backgroundart[0])
                    else:
                        logging.info("Background Art exists")

                    #BigPicture Art
                    if checkartworkexists(artwork_path, bigpictureart) == False:
                    
                        image_url = i['art_cover']
                        logging.info("Downloading BigPicture Art from " + image_url)
                        wget.download(image_url, out = artwork_path)
                        os.rename(artwork_path + '/' + image_url.split("/")[-1], artwork_path + '/' + bigpictureart[0])
                    else:
                        logging.info("BigPicture Art exists")
    except Exception:

        logging.critical(traceback.format_exc())

        if "deck" in os.path.expanduser("~"):
            if not settings.args.silent:
                os.system('zenity --error --title="Process Failed" --text="Failed to add artwork. Please check HeroicBashLauncher.log for the error in the HeroicBashLauncher folder and consider reporting it as an issue on GitHub." --width=400')
        else:
            if not settings.args.silent:
                os.system('zenity --error --title="Process Failed" --text="Failed to add artwork. Please check AddToSteam.log for the error in the HeroicBashLauncher folder and consider reporting it as an issue on GitHub." --width=400')    
        sys.exit()  
