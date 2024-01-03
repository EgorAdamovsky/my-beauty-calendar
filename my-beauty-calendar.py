import numpy as np
import datetime
import calendar
import ctypes
import cv2
import os

# ЧТЕНИЕ КОНФИГА
mycfg = open("config.txt", "r")
data = mycfg.readlines()
file = data[0].strip()
year = int(data[1])
_fc = data[2].split(',')
_bc = data[3].split(',')
_ec = data[4].split(',')
_nc = data[5].split(',')
fontcol = (int(_fc[2]), int(_fc[1]), int(_fc[0]))
backcol = (int(_bc[2]), int(_bc[1]), int(_bc[0]))
endcol = (int(_ec[2]), int(_ec[1]), int(_ec[0]))
nowcol = (int(_nc[2]), int(_nc[1]), int(_nc[0]))
over = float(data[6])
nowpoint = data[7]
mycfg.close()

# НАСТРОЙКИ
imsize = (1920, 1080)
offset = (1213, 160)
yearplace = (1440, 80)
cellsize = 28
tabsize = 230
tabpad = 16
table = 3
fontsize = 0.4
fontnums = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
fontyear = cv2.FONT_HERSHEY_TRIPLEX
fontmes = cv2.FONT_HERSHEY_COMPLEX
m = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# ПОДГОТОВКА
curday = datetime.datetime.now().day
curmonth = datetime.datetime.now().month
curyear = datetime.datetime.now().year
img = cv2.imread(file)
img = cv2.resize(img, imsize, img)
lay = np.zeros(shape=[imsize[1], imsize[0], 3], dtype=np.uint8)
cal = calendar.TextCalendar()

# ФОН И ВЫХОДНЫЕ
line, row, i, j = 0, 0, 0, 0
for moon in range(12):
    month = cal.monthdayscalendar(year, moon + 1)
    lay = cv2.rectangle(lay,
                        (offset[0] + tabsize * line + tabpad - cellsize,
                         offset[1] + tabsize * row + tabpad - int(2.5 * cellsize)),
                        (offset[0] + tabsize * line + tabsize - tabpad - int(0.5 * cellsize),
                         offset[1] + tabsize * row + tabsize - tabpad - int(2 * cellsize)),
                        backcol, -1)
    for week in month:
        dofw = 0
        for day in week:
            dofw += 1
            if day != 0:
                if dofw > 5:
                    lay = cv2.circle(lay,
                                     (offset[0] + tabsize * line + cellsize * j + int(cellsize / 3.5),
                                      offset[1] + tabsize * row + cellsize * i - int(cellsize / 6)),
                                     int(30 * fontsize), endcol, -1)
            j += 1
        i += 1
        j = 0
    line += 1
    i, j = 0, 0
    if line == table:
        line = 0
        row += 1
img = cv2.addWeighted(img, 1, lay, over, 0)

# ТЕКСТ
cv2.putText(img, str(year), yearplace, fontyear, 2.5, fontcol)
line, row, i, j, ch = 0, 0, 0, 0, 0
for moon in range(12):
    month = cal.monthdayscalendar(year, moon + 1)

    # месяцы
    for week in month:
        cv2.putText(img, m[moon],
                    (tabsize * line + offset[0],
                     tabsize * row + offset[1] - cellsize),
                    fontmes, 1.5 * fontsize, fontcol)

        # дни
        for day in week:
            ch += 1

            # дни месяца
            if day != 0:
                fullday = 0
                if day < 10:
                    fullday = 4
                cv2.putText(img, str(day),
                            (offset[0] + tabsize * line + cellsize * j + fullday,
                             offset[1] + tabsize * row + cellsize * i),
                            fontnums, fontsize, fontcol)

            # текущий день
            if nowpoint == "true":
                if ch == curday and moon + 1 == curmonth and curyear == year:
                    img = cv2.circle(img,
                                     (offset[0] + tabsize * line + cellsize * j + int(cellsize / 3.5),
                                      offset[1] + tabsize * row + cellsize * i - int(cellsize / 6)),
                                     int(28 * fontsize), nowcol, 2)
            j += 1
        i += 1
        j = 0
    line += 1
    i, j, ch = 0, 0, 0
    if line == table:
        line = 0
        row += 1

# СОХРАНЕНИЕ
fout = "calendar-" + str(year) + ".png"
cv2.imwrite(fout, img)

# УСТАНОВКА НА РАБОЧИЙ СТОЛ
ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(os.curdir) + "\\" + fout, 0)

# ТЕСТ
# img = cv2.resize(img, (960, 540))
# cv2.imshow("", img)
# cv2.waitKey()

print("Готово!")
