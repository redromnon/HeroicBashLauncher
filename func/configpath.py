'''
CONTAINS VARIABLES THAT HOLD PATH TO RESPECTIVE CONFIG FILES' LOCATION

Heroic

/.config/heroic/GamesConfig || /.var/app/com.heroicgameslauncher.hgl/config/heroic/GamesConfig

/.config/legendary/installed.json || /.var/app/com.heroicgameslauncher.hgl/config/legendary/installed.json


GOG

/.config/heroic/gog_store/installed.json || /.var/app/com.heroicgameslauncher.hgl/config/heroic/gog_store/installed.json

/.config/heroic/gog_store/library.json || /.var/app/com.heroicgameslauncher.hgl/config/heroic/gog_store/library.json

'''
import os

is_flatpak = False

gamesjsonpath = os.path.expanduser("~") + "/.config/heroic/GamesConfig"

heroicconfigpath = os.path.expanduser("~") + "/.config/heroic/config.json"

legendaryinstalledpath = os.path.expanduser("~") + "/.config/legendary/installed.json"

goginstalledpath = os.path.expanduser("~") + "/.config/heroic/gog_store/installed.json"

goglibrarypath = os.path.expanduser("~") + "/.config/heroic/gog_store/library.json"

heroiclibrarypath = os.path.expanduser("~") + "/.config/heroic/lib-cache/library.json"


#Check if Flatpak exists
if os.path.exists(os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl"):

    is_flatpak = True

    gamesjsonpath = os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/config/heroic/GamesConfig"

    heroicconfigpath = os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/config/heroic/config.json"

    legendaryinstalledpath = os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/config/legendary/installed.json"

    goginstalledpath = os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/config/heroic/gog_store/installed.json"

    goglibrarypath = os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/config/heroic/gog_store/library.json"

    heroiclibrarypath = os.path.expanduser("~") + "/.var/app/com.heroicgameslauncher.hgl/config/heroic/lib-cache/library.json"