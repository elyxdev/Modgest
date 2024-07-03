import os
if os.name == "nt":
    os.system("pyinstaller --clean --onefile --name Modgest_Win --icon .\img\modgest.ico mod_gest.py")
else:
    os.system("pyinstaller --clean --onefile --name modgest mod_gest.py")