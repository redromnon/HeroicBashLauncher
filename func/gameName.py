#Helps name the bash files (launch files) with the game's actual name

def getnameofgame(realgamename):
    
    name = ""

    for char in realgamename:

        letter = char.isalpha()

        if letter == True:

            name = name + char

    return name
