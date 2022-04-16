#!/bin/env python3
#Main file that takes bash arguments

import os, sys, argparse
import configpath
from frombash import frombash
from listinstalled import listinstalled
from steam import createscript, addtosteam
from flatpak import launchflatpakgame
from zenity import zenity_popup, zenity_enable

#Print current version
print("Using Bash Launcher 2.4.2\n")

parser = argparse.ArgumentParser(description='Create launcher scripts from games installed with Heroic')
parser.add_argument("--zenity", action="store_true",
                    help="Enable zenity popups showing status as well as printing to stdout")
group = parser.add_mutually_exclusive_group()
group.add_argument("--create_all", action="store_true",
                    help="List installed Heroic games, create launch files, and add them all to Steam")
group.add_argument("--create", metavar="gamename", type=str,
                    help="Create a single launch file for gamename, and add it to Steam")
# catch-all for backwards compatibility
parser.add_argument("rest", nargs="*",
                    help="[gamename appname gamejson gametype] or [gamename appname gamejson gametype flatpak]")
args = parser.parse_args()
# whether we use zenity or not
zenity_enable(enable=args.zenity)

if (os.path.exists(configpath.legendaryinstalledpath) == True or os.path.exists(configpath.goginstalledpath) == True):

    #If len of arguments is 1 (no extra arguements), then proceed to create launch files for all games
    #   else, update parameters of a game through launch file

    #print("rest:", args.rest)

    if len(args.rest) == 0 or args.create_all:
        #Only name of file as default argument
    
        listinstalled()

        #Don't create AddToSteam script if Steam Deck 
        if "deck" in os.path.expanduser("~"):
            zenity_popup(title="Process Finished", text="Launch scripts stored in GameFiles folder\n\nYour games have been synced to Steam\n\nHave fun gaming!")
        else:
            zenity_popup(title="Process Finished", text="Launch scripts stored in GameFiles folder\n\nYou can sync games to Steam via AddToSteam\n\nHave fun gaming!")
            print("\nCreating AddToSteam script...")
            createscript()

    elif len(args.rest) == 1 or args.create is not None:
        #Contains simplified gamename as arg for Steam addition
        if args.create is not None:
            gamename = args.create
        else:
            gamename = args.rest[0]
        if len(gamename) == 0:
            print("No game selected")
            sys.exit(-1)
        else:
            addtosteam(gamename)

    elif len(args.rest) == 4:
        # Run from launch script
        gamename, appname, gamejson, gametype = args.rest
        frombash(gamename, appname, gamejson, gametype)

    elif len(args.rest) == 5:
        # Run from launch script: flatpak version
        gamename, appname, gamejson, gametype, flatpak = args.rest
        launchflatpakgame(gamename, appname, gamejson, gametype, flatpak)

    else:
        parser.print_help()
        zenity_popup(type="error", title="Invalid Args", text="Invalid args passed to script, check log file and consider filing a bug")
        sys.exit(-1)

else:
    zenity_popup(type="error", title="Process Stopped", text="Looks like you have not installed Heroic Games Launcher or installed any game\n\nPlease consider doing so and try again")

