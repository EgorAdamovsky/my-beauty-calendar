from pyshortcuts import make_shortcut
import getpass
import os

user = getpass.getuser()
base_path = os.path.abspath(os.curdir) + "/dist"
file_path = base_path + "/my-beauty-calendar.exe"
link_path = "C:/Users/" + user + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/"
make_shortcut(script=file_path, name='my-beauty-calendar', folder=link_path, working_dir=base_path)
print("Готово!")
