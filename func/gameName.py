#Remove special characters from game names (caused errors when using encode()/decode())
def rspchar(realgamename):

    name = ""

    #Include the following characters
    includechar = [" ", "'", ":", "(", ")"]

    for char in realgamename:

        if char.isalnum() == True or char in includechar:

            name = name + char

    return name

#Name launch script
def filegamename(realgamename):

    name = ""

    for char in realgamename:

        if char.isalnum() == True:

            name = name + char

    #Labeling this game as a Heroic game for naming file
    name = name + "_Heroic"

    return name
