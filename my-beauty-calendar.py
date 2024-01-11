from PIL import ImageFont, ImageDraw, Image
import numpy as np
import datetime
import calendar
import ctypes
import time
import cv2
import os

# ПРИКОЛ
microsleep = 0.25
print("\n")
print("\t██   ██ ██    ██  ██████ ██   ██  █████       ██████   █████  ███    ███ ███████ ███████")
time.sleep(microsleep)
print("\t██  ██  ██    ██ ██      ██   ██ ██   ██     ██       ██   ██ ████  ████ ██      ██")
time.sleep(microsleep)
print("\t█████   ██    ██ ██      ███████ ███████     ██   ███ ███████ ██ ████ ██ █████   ███████")
time.sleep(microsleep)
print("\t██  ██  ██    ██ ██      ██   ██ ██   ██     ██    ██ ██   ██ ██  ██  ██ ██           ██")
time.sleep(microsleep)
print("\t██   ██  ██████   ██████ ██   ██ ██   ██      ██████  ██   ██ ██      ██ ███████ ███████")
time.sleep(4 * microsleep)

# ЧТЕНИЕ КОНФИГА
mycfg = open("config.txt", "r")  # прочитать файл конфигов
data = mycfg.readlines()  # прочитать все строки
file = data[0].strip()  # адрес картинки
year = int(data[1])  #
_fc = data[2].split(',')  #
_bc = data[3].split(',')  #
_ec = data[4].split(',')  #
_nc = data[5].split(',')  #
fontcol = (int(_fc[0]), int(_fc[1]), int(_fc[2]))  #
backcol = (int(_bc[2]), int(_bc[1]), int(_bc[0]))  #
endcol = (int(_ec[2]), int(_ec[1]), int(_ec[0]))  #
nowcol = (int(_nc[2]), int(_nc[1]), int(_nc[0]))  #
over = float(data[6])  #
nowpoint = data[7].strip()  #
roundbias = int(data[8])  #
blur = int(data[9])  #
fordesktop = data[10].strip()  #
noworks = data[11].strip()  #
todesk = data[12].strip()  #
mycfg.close()  #

# НАСТРОЙКИ
deskoffset = 5 if fordesktop == "true" else 20
imsize = (1920, 1080)
offset = (1213, 160 + deskoffset)
yearplace = (1445, 10 + deskoffset)
cellsize = 28
tabsize = 230
tabpad = 16
table = 3
fontsize = 0.4
fontkoef = 38
fontname = "ubuntu.ttf"
pilfontsize = ImageFont.truetype(fontname, int(fontkoef * fontsize))
pilfontsizemonth = ImageFont.truetype(fontname, int(1.25 * fontkoef * fontsize))
pilfontsizeyear = ImageFont.truetype(fontname, int(6 * fontkoef * fontsize))
m = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

# ПОДГОТОВКА
noworksdaysint = []
curday = datetime.datetime.now().day
curmonth = datetime.datetime.now().month
curyear = datetime.datetime.now().year
img = cv2.imread(file)
img = cv2.resize(img, imsize, img)
lay = np.zeros(shape=[imsize[1], imsize[0], 3], dtype=np.uint8)
cal = calendar.TextCalendar()
noworksdays = open(noworks, "r").readlines()
for i in range(len(noworksdays)):
    noworksdays[i] = noworksdays[i].strip()
    temp = noworksdays[i].split('.')
    noworksdaysint.append([int(temp[0]), int(temp[1])])

# ФОН И ВЫХОДНЫЕ ДНИ
line, row, i, j = 0, 0, 0, 0
for moon in range(12):

    # плитки месяцев
    month = cal.monthdayscalendar(year, moon + 1)
    x1 = offset[0] + tabsize * line + tabpad - cellsize
    y1 = offset[1] + tabsize * row + tabpad - int(2.5 * cellsize)
    x2 = offset[0] + tabsize * line + tabsize - tabpad - int(0.5 * cellsize)
    y2 = offset[1] + tabsize * row + tabsize - tabpad - int(2 * cellsize)
    lay = cv2.rectangle(lay, (x1 + roundbias, y1), (x2 - roundbias, y2), backcol, -1)
    lay = cv2.rectangle(lay, (x1, y1 + roundbias), (x2, y2 - roundbias), backcol, -1)
    lay = cv2.circle(lay, (x1 + roundbias, y1 + roundbias), roundbias, backcol, -1)
    lay = cv2.circle(lay, (x1 + roundbias, y2 - roundbias), roundbias, backcol, -1)
    lay = cv2.circle(lay, (x2 - roundbias, y1 + roundbias), roundbias, backcol, -1)
    lay = cv2.circle(lay, (x2 - roundbias, y2 - roundbias), roundbias, backcol, -1)

    # кружочки выходных и праздников
    for week in month:  # цикл по неделям месяца
        dofw = 0  # счетчик дня недели
        for day in week:  # цикл по дням недели
            dofw += 1  # инкремент счетчика дня недели
            if day != 0:  # если текущий день присутствует в месяце
                holiday = False  # по умолчанию день рабочий
                for nwd in noworksdaysint:  # цикл по праздничным дням
                    if nwd[0] == day and nwd[1] == moon + 1:  # если текущий день месяца праздничный
                        holiday = True  # ставится отметка
                        break  # дальнейшая проверка не требуется
                if dofw > 5 or holiday:  # если день выходной или праздничный
                    wx = offset[0] + tabsize * line + cellsize * j + int(cellsize / 3.5)  # смещение кружка по X
                    wy = offset[1] + tabsize * row + cellsize * i - int(cellsize / 6)  # смещение кружка по Y
                    lay = cv2.circle(lay, (wx, wy), int(30 * fontsize), endcol, -1)  # отрисовка кружка
            j += 1
        i += 1
        j = 0
    line += 1
    i, j = 0, 0
    if line == table:
        line = 0
        row += 1

# БЛЮР ПЛИТОК
imgblur = cv2.blur(img, (blur, blur))
imgtemp = 0 * img
imgtemp += imgblur * (lay > 0) + img * (lay == 0)
img = imgtemp

# СМЕШЕНИЕ СЛОЕВ
img = cv2.addWeighted(img, 1, lay, over, 0)

# ТЕКСТ
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
pilimg = Image.fromarray(img)
draw = ImageDraw.Draw(pilimg)
draw.text(yearplace, str(year), font=pilfontsizeyear, fill=fontcol, align="center")  # нарисовать год
line, row, i, j, ch = 0, 0, 0, 0, 0
for moon in range(12):
    month = cal.monthdayscalendar(year, moon + 1)

    # недели месяца
    for week in month:
        wx = tabsize * line + offset[0]
        wy = tabsize * row + offset[1] - cellsize - 18

        ims = 0
        for ms in m[moon]:
            draw.text((wx + ims, wy), ms, font=pilfontsizemonth, fill=fontcol, align="center")  # нарисовать год
            ims += 10

        # дни
        for day in week:
            ch += 1

            # дни месяца
            if day != 0:  # если день есть в месяце
                fullday = 1  # смещение для однозначного числа
                if day < 10:  # если число-таки однозначное
                    fullday = 5  # смещение становится ненулевым
                dwx = offset[0] + tabsize * line + cellsize * j + fullday  # точка отрисовки числа по X
                dwy = offset[1] + tabsize * row + cellsize * i - 12  # точка отрисовки числа по Y
                draw.text((dwx, dwy), str(day), font=pilfontsize, fill=fontcol, align="center")  # нарисовать число

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
img = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)

# ТЕКУЩИЙ ДЕНЬ
line, row, i, j, ch = 0, 0, 0, 0, 0
for moon in range(12):
    month = cal.monthdayscalendar(year, moon + 1)
    for week in month:
        for day in week:
            ch += 1

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
fout = "calendar-" + str(year) + ".png"  # название выходного изображения
cv2.imwrite(fout, img)  # сохранить изображение

# УСТАНОВКА НА РАБОЧИЙ СТОЛ
if todesk == "true":  # если включена соответствующая опция
    imgpath = os.path.abspath(os.curdir) + "\\" + fout  # определение пути к изображению
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imgpath, 0)  # установить его на рабочий стол

# ТЕСТ
# img = cv2.resize(img, (960, 540))
# cv2.imshow("low-size test", img)
# cv2.waitKey()
