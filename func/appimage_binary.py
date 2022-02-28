#For AppImage, check if alternavtive binary (Legendary) is added.
#If not, check folder under /tmp/ that includes path to the binaries.

import os, json

def getlegendaryappimage():
    
    legendary_path = os.getcwd() + "/legendary "

    return legendary_path
