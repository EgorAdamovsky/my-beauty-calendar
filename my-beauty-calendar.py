import numpy as np
import datetime
import calendar
import ctypes
import cv2
import sys
import os

# АРГУМЕНТЫ: ФАЙЛ ГОД ЦВЕТ-ТЕКСТА ЦВЕТ-ФОНА ЦВЕТ-ВЫХОДНЫХ ЦВЕТ-ТЕКУЩЕГО ПРОЗРАЧНОСТЬ
file = sys.argv[1]
year = int(sys.argv[2])
_fc = sys.argv[3].split(',')
_bc = sys.argv[4].split(',')
_ec = sys.argv[5].split(',')
_nc = sys.argv[6].split(',')
fontcol = (int(_fc[2]), int(_fc[1]), int(_fc[0]))
backcol = (int(_bc[2]), int(_bc[1]), int(_bc[0]))
endcol = (int(_ec[2]), int(_ec[1]), int(_ec[0]))
nowcol = (int(_nc[2]), int(_nc[1]), int(_nc[0]))
over = float(sys.argv[7])

# НАСТРОЙКИ
imsize = (1920, 1080)
offset = (1147, 100)
cellsize = 32
tabsize = 256
tabpad = 16
table = 3
fontsize = 0.5
font = cv2.FONT_HERSHEY_COMPLEX
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
                                     (offset[0] + tabsize * line + cellsize * j + int(cellsize / 3),
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
cv2.putText(img, str(year), (50, 1030), cv2.FONT_HERSHEY_TRIPLEX, 3, fontcol)
line, row, i, j, ch = 0, 0, 0, 0, 0
for moon in range(12):
    month = cal.monthdayscalendar(year, moon + 1)
    for week in month:
        cv2.putText(img, m[moon],
                    (tabsize * line + offset[0],
                     tabsize * row + offset[1] - cellsize),
                    font, fontsize, fontcol)
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
                            font, fontsize, fontcol)

            # текущий день
            if ch == curday and moon + 1 == curmonth and curyear == year:
                img = cv2.circle(img,
                                 (offset[0] + tabsize * line + cellsize * j + int(cellsize / 3),
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

# ОТОБРАЖЕНИЕ
# cv2.imshow("", img)
# cv2.waitKey()

# УСТАНОВКА НА РАБОЧИЙ СТОЛ
ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(os.curdir) + "\\" + fout, 0)
print("Готово!")
