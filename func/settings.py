#CREATE/READ JSON FILE AND APPLY SETTINGS

import os, json, logging

#Declare
enable_epic = None
enable_artwork = None
enable_gog = None
enable_autoaddtosteam = None

#Create settings.config file
def create_settings_file():
        
    dictvalues = {
        "artwork": True,
        "epic": True,
        "gog": True,
        "autoaddtosteam": True
    }

    if not os.path.isfile('settings.config'):

        logging.warning("Settings config file not found.")

        with open('settings.config', 'w') as sc:
            json.dump(dictvalues, sc, indent=2)
            logging.info("Settings config file created.")


#Read settings values
def read_settings_file():
    with open('settings.config', 'r') as sr:
        setting = json.load(sr)

    global enable_epic, enable_artwork, enable_gog, enable_autoaddtosteam
    enable_artwork = setting["artwork"]
    enable_epic = setting["epic"]
    enable_gog = setting["gog"]

    try:
        enable_autoaddtosteam = setting["autoaddtosteam"]
    except:
        logging.warning("addtosteam setting not found, adding to config file...")
        setting["autoaddtosteam"] = True
        with open('settings.config', 'w') as sc:
            json.dump(setting, sc, indent=2)
            logging.info("Settings config file updated.")
