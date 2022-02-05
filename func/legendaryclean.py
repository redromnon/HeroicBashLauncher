#Cleans temorary files and leftovers

import os;

def legendaryclean():

    #Clean leftover files
    print("\nCleaning left over game files if any...")
    os.system("/opt/Heroic/resources/app.asar.unpacked/build/bin/linux/legendary cleanup")