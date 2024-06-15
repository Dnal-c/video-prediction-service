from fastapi import APIRouter, HTTPException, Response, UploadFile, status, File, Header, Body, Depends, Form

import global_context
from controller.common import predictions_to_response
from global_env import POSSIBLE_FILE_SIZE
from service.minio_client import upload_file
from predict import predict_by_video

SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

router = APIRouter(tags=['Предсказание по видео. Версия для работы с File'])


@router.post('/predict-by-file')
async def predict(description: str = Form(...), file_data: UploadFile = File(...)):
    link = upload_file_to_minio(file_data)

    predictions = predict_by_video.predict(link, description)
    global_context.elastic_service.save_prediction(predictions)

    return predictions_to_response(predictions)


def is_valid_file(size):
    if not 0 < size <= POSSIBLE_FILE_SIZE:
        return False
    return True


def upload_file_to_minio(file_data):
    if not file_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Файл не передан'
        )
    file = file_data.file
    file_extension = file_data.filename.split('.')[-1]

    contents = file.read()
    size = len(contents)
    is_valid = is_valid_file(size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В данный момент возможна загрузка файлов менее 50мб'
        )

    return upload_file(size, contents, file_extension)
