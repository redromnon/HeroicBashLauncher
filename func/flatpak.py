import os


#SET PATH TO GAME'S LAUNCH SCRIPT IN FLATPAK
def getflatpakpath(flatpakpath):
   
    #Count no. of "/"
    count = 0
    c = 0

    for i in flatpakpath:
        if count == 3:
            c = flatpakpath.index(i)
            break

        if i == "/":
            count = count + 1
    
    #print(count)

    return flatpakpath[c:]

          