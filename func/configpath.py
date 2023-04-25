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
import subprocess

HGL_FLATPAK_APPID = "com.heroicgameslauncher.hgl"
STEAM_FLATPAK_APPID = "com.valvesoftware.Steam"

flatpak_base_config_path = os.path.join(os.path.expanduser("~/.var/app/"), HGL_FLATPAK_APPID, "config")
# Electron's app.getPath("appData") in Heroic Games Launcher will use XDG_CONFIG_HOME if it is set.
native_base_config_path = os.environ.get("XDG_CONFIG_HOME") if os.environ.get("XDG_CONFIG_HOME") else os.path.expanduser("~/.config")


def is_flatpak_installed(application_id: str) -> bool:
    """Given an application ID, returns if the flatpak is installed  and has been run once 
    based on the output of the flatpak list command and the presence of the config folder"""
    try:
        r = subprocess.run(["flatpak", "list", "--columns=application"], capture_output=True)
        return (r.returncode == 0 and # Flatpak command ran successfully
            application_id in r.stdout.decode().splitlines() and  # Application ID is installed in Flatpak
            os.path.exists(os.path.join(os.path.expanduser("~/.var/app/"), application_id)) # Config is present
            )
    except FileNotFoundError:
        # flatpak command was not found
        return False

#Check if Flatpak exists
if is_flatpak_installed(HGL_FLATPAK_APPID): # Heroic is installed and config is present
    is_flatpak = True
    actual_config_path = flatpak_base_config_path
else:
    is_flatpak = False
    actual_config_path = native_base_config_path

gamesjsonpath = os.path.join(actual_config_path, "heroic/GamesConfig")

heroicconfigpath = os.path.join(actual_config_path, "heroic/config.json")

legendaryinstalledpath = os.path.join(actual_config_path, "legendary/installed.json")

goginstalledpath = os.path.join(actual_config_path, "heroic/gog_store/installed.json")

goglibrarypath = os.path.join(actual_config_path, "heroic/store_cache/gog_library.json")

heroiclibrarypath = os.path.join(actual_config_path, "heroic/lib-cache/library.json")

timestamppath = os.path.join(actual_config_path, "heroic/store/timestamp.json")

storejsonpath = os.path.join(actual_config_path, "heroic/store/config.json")

runtimepath = os.path.join(actual_config_path, "heroic/tools/runtimes/")

# Check if Steam is Flatpak
is_steam_flatpak =  is_flatpak_installed(STEAM_FLATPAK_APPID)
