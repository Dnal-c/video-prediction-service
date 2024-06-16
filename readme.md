# video-prediction-service
Данный репозиторий нужен для того, чтобы осуществлять инференс нашего флоу и считать фичи по видео

Структура пакетов:

<pre>
├── automatic_speech_recognition - содержит код для распознования текста с видео
├── controller - здесь прием http-запросов
├── deploy - ci/cd
├── image_captioning - содержит код для распознавания текста с видео
├── models - модели для работы локально
├── predict - код для расчета фичей
├── service - сервис слой. Внутри обращение к elastic, minio и рассчет embedding'ов
├── translate - код для перевода с английского на русский
├── requirements.txt - зависимости
├── global_context.py - сквозные вещи, которые используются в разных пакетах сервиса
└── global_env.py - конфигурационные переменные
</pre>


# Инструкция для работы локально кратко
В global.env BASE_DIR_PATH - прокинуть путь до директории с проектом
В models запустить [models_to_local.py](models%2Fmodels_to_local.py) 

в service в [elastic.py](service%2Felastic.py), [minio_client.py](service%2Fminio_client.py)
прокинуть креды для коннектов 

запустить [main.py](main.py)main.py