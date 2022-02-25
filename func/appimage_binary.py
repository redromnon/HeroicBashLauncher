
import os 

def getlegendaryappimage():
    list = os.listdir('/tmp/')

    heroic_path = ""

    for i in list:
        if "Heroic" in i:
            #print(i)
            heroic_path = '/tmp/' + i + '/resources/app.asar.unpacked/build/bin/linux/legendary '
            break

    return heroic_path



