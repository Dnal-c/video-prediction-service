import torch
from dotenv import load_dotenv

load_dotenv()

MINIO_URL = '87.242.93.110:9000'
MINIO_BUCKET = 'our-bucket'
MINIO_KEY = 'UIY9icUCtWfkGNU6sZM3'
MINIO_SECRET_KEY = 'W6z8XLLFYyP4K0NIoBXFmCez1PTjnJvWbXWEjH0d'
POSSIBLE_FILE_SIZE = 52428800
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Если запуск идет с CPU, то необходимо float32 или float16, на GPU можно пробовать int8, float16, float32
WHISPER_COMPUTE_TYPE = "int8" if DEVICE == "gpu" else "float32"


BASE_DIR_PATH = '/Users/apple/Documents/projects/hackaton-lct-2024/video-prediction-service'
MODEL_CAPTION_PATH = BASE_DIR_PATH + '/models/captioning'  # нужен для локальной работы с image captioning
MODEL_TRANSLATOR_PATH = BASE_DIR_PATH + '/models/translator'  # нужен для локальной работы с automatic speech recogni


TEMP_DIRECTORY_PATH = '/Users/apple/Documents/projects/hackaton-lct-2024/video-prediction-service/images'  # Параметр, отвечающий за то, куда будем складывать файлы

SAVING_FRAMES_PER_SECOND = .25  # Параметр, отвечающий за то, сколько фреймов с видео резать за секунду для обработки