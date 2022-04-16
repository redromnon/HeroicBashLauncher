import os,sys

#Check if Zenity is installed
_check_zenity = os.system('zenity --version')
_use_zenity = False

def zenity_installed():
    return _check_zenity == 0

def zenity_enable(enable=None):
    """
    Enable/disable the use of zenity popups.
    """
    global _use_zenity
    if enable is not None:
        _use_zenity = enable and zenity_installed()
    return _use_zenity

def zenity_popup(title, text, type="info", width=300):
    if zenity_enable():
        os.system('zenity --{} --title="{}" --text="{}" --width={}'.format(type, title, text, width))
    else:
        print("\n\n{}:\n{}".format(title, text))

