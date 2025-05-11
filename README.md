# Label Studio для датасетов робота-андроида

Этот репозиторий содержит инструменты для обработки и управления датасетами в Label Studio, специально разработанные для задач обнаружения и распознавания лиц.

## Project Structure

```
.
├── manipulations/
│   ├── generate_label_studio_import.py  # Генерирует файл импорта для Label Studio
│   └── process_label_studio_export.py   # Обрабатывает экспортированные данные из Label Studio и создаёт датасет из вырезанных лиц
├── label-studio-files/
│   ├── dataset/                        # Директория с исходными изображениями
│   └── cropped_dataset/                # Директория с обработанными изображениями лиц
└── data/
    └── label_studio_import.json        # Сгенерированный файл импорта для Label Studio
```

## Требования

- Python 3.12+
- OpenCV (cv2)
- Запущенный экземпляр Label Studio

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/basalegend/label-studio-robot-android.git
cd label-studio-robot-android
```

2. Установите необходимые зависимости:
```bash
pip install opencv-python
```

## Использование


## Запуск Label Studio

### Вариант 1: Использование docker-compose

Проект включает поддержку Docker для запуска Label Studio. Используйте предоставленный `docker-compose.yml`:

```bash
docker-compose up -d
```

Это запустит Label Studio на порту 8080.

### Вариант 2: Использование Dockerfile

1. Создайте необходимые директории:
```bash
mkdir -p label-studio-data label-studio-files
```

2. Соберите Docker образ:
```bash
docker build -t label-studio-custom .
```

3. Запустите контейнер:
```bash
docker run -d \
  --name label_studio_container \
  -p 8080:8080 \
  -v ./label-studio-data:/label-studio/data \
  -v ./label-studio-files:/label-studio/files \
  label-studio-custom
```

После запуска Label Studio будет доступен по адресу http://localhost:8080

### 1. Подготовка данных для Label Studio

Используйте `generate_label_studio_import.py` для создания файла импорта в Label Studio:

```bash
python manipulations/generate_label_studio_import.py
```

Этот скрипт:
- Сканирует директорию `label-studio-files/dataset/`
- Находит все JPG и PNG изображения
- Генерирует JSON файл в формате, совместимом с импортом Label Studio
- Сохраняет результат в `data/label_studio_import.json`

### 2. Обработка экспорта из Label Studio

После разметки в Label Studio используйте `process_label_studio_export.py` для обработки экспортированных данных:

```bash
python manipulations/process_label_studio_export.py
```

Этот скрипт:
- Читает JSON файл экспорта из Label Studio
- Извлекает области лиц на основе аннотаций
- Сохраняет обрезанные лица в `label-studio-files/cropped_dataset/`
- Организует лица по именам людей

## Структура директорий

- `label-studio-files/dataset/`: Разместите здесь исходные изображения, организованные по именам людей
- `label-studio-files/cropped_dataset/`: Здесь будут сохранены обработанные изображения лиц
- `data/`: Содержит сгенерированные файлы импорта/экспорта

## Форматы файлов

### Входной формат
- Изображения должны быть в формате JPG или PNG
- Изображения должны быть организованы в папки по именам людей
- Пример структуры:
```
label-studio-files/dataset/
├── person1/
│   ├── image1.jpg
│   └── image2.jpg
└── person2/
    ├── image1.jpg
    └── image2.jpg
```

### Выходной формат
- Обработанные лица сохраняются как JPG файлы
- Файлы именуются как `{имя_человека}_{счетчик}.jpg`
- Пример: `person1_01.jpg`, `person1_02.jpg` и т.д.
