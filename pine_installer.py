import os
print("Welcome to Pine installer!")
print("Installer version: v0.1")
print("Version to be installed: v0.1")
print("Press [Enter] to continue...")
print("Type in 's' to run with admin privileges... (uses sudo)")
user = input()
if user == "s":
    os.system("sudo pip install PyQT5")
    print("Installed PyQT5")
    os.system("sudo pip install PyQtWebEngine")
    print("Installed PyQtWebEngine")
else:
    os.system("pip install PyQT5")
    print("Installed PyQT5")
    os.system("pip install PyQtWebEngine")
    print("Installed PyQtWebEngine")
print("Installation complete!")
print("Press [Enter] to exit...")
print("Press [r] to run Pine...")
user = input()
if user == "r":
    os.system("python pine.py")
else:
    exit()