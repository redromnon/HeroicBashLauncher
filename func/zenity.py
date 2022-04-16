
import os,sys

#Check if Zenity is installed
checkzenity = os.system('zenity --version')

def zenity_popup(title, text, type="info", width=300):
    if checkzenity == 0 and "deck" not in os.path.expanduser("~"):
        os.system('zenity --{} --title="{}" --text="{}" --width={}'.format(type, title, text, width))
    else:
        print("\n\n{}:\n{}".format(title, text))

