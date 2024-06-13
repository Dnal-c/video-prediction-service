from fastapi import APIRouter, HTTPException, Response, UploadFile, status, File, Header, Body, Depends

import global_context
from global_env import POSSIBLE_FILE_SIZE
from service.minio_client import upload_file
from pydantic import BaseModel
from predict import predict_by_video


async def minio_upload(contents: bytes, key: str):
    print('')


# async def minio_download(key: str):
#     try:
#         return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
#     except ClientError as err:
#         logger.error(str(err))

class Options(BaseModel):
    link: str
    description: str


SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}

router = APIRouter(prefix='/api/v1', tags=['our api'])


@router.post('/upload-file')
async def upload(options: Options = Depends(), file_data: UploadFile = File(...)):
    data_options = options.dict()

    link = data_options.get('link')
    description = data_options.get('description')
    if link is None:
        print('Ссылка не передана')
        link = upload_file_to_minio(file_data)
    predictions = predict_by_video.predict(link, description)

    # TODO сюда код сохранения предикшнов в эластик, пример того, как выглдит дескрипшн сейчас ниже. Код, где собирается в таком виде - predict_by_video.predict
    '''
    '''
    global_context.elastic_service.save_prediction(predictions)

    return predictions


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
