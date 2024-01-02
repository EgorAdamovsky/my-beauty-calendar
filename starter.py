import getpass
import sys
import os

# АРГУМЕНТЫ: КАРТИНКА ГОД ЦВЕТ-ТЕКСТА ЦВЕТ-ФОНА ЦВЕТ-ВЫХОДНЫХ ЦВЕТ-ТЕКУЩЕГО ПРОЗРАЧНОСТЬ
args = ""
for i in range(8):
    if i > 0:
        args += sys.argv[i] + " "

user = getpass.getuser()
base_path = os.path.abspath(os.curdir)
file_path = base_path + "\\dist\\my-beauty-calendar.exe"
bat_path = "C:\\Users\\" + user + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
with open(bat_path + '\\' + "my-beauty-calendar.bat", "w+") as bat_file:
    bat_file.write('start "" ' + file_path + " " + args)

print("Готово!")
