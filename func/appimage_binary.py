#For AppImage, check if alternavtive binary (Legendary) is added.
#If not, check folder under /tmp/ that includes path to the binaries.

import os, json, re 

def getlegendaryappimage():
    
    legendary_path = ""

    #Path to heroic's  where each installed game's json is stored
    heroicconfigpath = os.path.expanduser("~") + "/.config/heroic/config.json"

    #Path to tmp dir
    list = os.listdir('/tmp/')

    #Convert config json to dict
    with open(heroicconfigpath) as p:
      heroicconfig = json.load(p)

    #If legendary binary doesn't exist, check for temp folder
    if heroicconfig["defaultSettings"]["altLegendaryBin"] == "":
        
        for i in list:
            if re.search("Heroic", i) != None:
                #print(i)
                legendary_path = '/tmp/' + i + '/resources/app.asar.unpacked/build/bin/linux/legendary '
                break
    else:

        legendary_path = heroicconfig["defaultSettings"]["altLegendaryBin"] + " "

    return legendary_path


