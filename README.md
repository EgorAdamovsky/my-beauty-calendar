# Генератор календаря на рабочий стол

### 1. Что это?
Набор Py-скриптов для генерации календаря на рабочий стол.

### 2. Возможности:
- выбор фонового изображения 1920х1080 px;
- выбор произвольного года;
- выбор цвета текста и подложки;
- отображение текущей даты (опционально);
- автоматическое обновление рабочего стола.

### 3. Пример:
![Результат](/other/calendar-2024.png)

## Инструкция:
1. Установите необходимые модули:

```shell
pip install -r requirements.txt
```

2. Подготовьте файл конфигурации **config.txt**, который должна быть каталоге с приложением/скриптом:
    - **example.jpg** - путь к изображению Full HD качества;
    - **2024** - выбранный год;
    - **0,0,0** - цвет текста в модели RGB;
    - **255,255,255** - цвет плиток в модели RGB;
    - **64,64,64** - цвет меток выходных дней в модели RGB;
    - **0,0,0** - цвет метки текущей даты в модели RGB;
    - **0.125** - непрозрачность фона;
    - **true** - отображение текущей даты;
    - **15** - радиус скругления плиток;
    - **9** - степень размытия фона под плитками;
    - **true** - смещение календаря под нижнюю панель приложений.
```
example.jpg
2024
0,0,0
255,255,255
64,64,64
0,0,0
0.125
true
15
9
true
```

3. Если хотите протестировать алгоритм, то запустите **my-beauty-calendar.py**. Иначе пропустите этот пункт:
```shell
python my-beauty-calendar.py
```

3. Сгенерируйте исполняемый файл:
```shell
pyinstaller --onefile my-beauty-calendar.py
``` 

4. Скопируйте в каталог с приложением **my-beauty-calendar.exe** файл **config.txt**:
```
...\my-beauty-calendar\dist\my-beauty-calendar.exe
```

5. Запустите **starter.py** для добавления возможности автозапуска:
```shell
python starter.py
```

Теперь при каждом старте Windows изображение будет обновляться самостоятельно.
