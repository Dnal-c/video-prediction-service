import os
from datetime import timedelta

from minio import Minio

import uuid
from io import BytesIO

# Create the client
client = Minio(
    endpoint=os.environ['MINIO_URL'],
    access_key=os.environ['MINIO_KEY'],
    secret_key=os.environ['MINIO_SECRET_KEY'],
    secure=False
)


def upload_file(length, file_data, file_extension):
    random_uuid = uuid.uuid4()
    file_name = 'file' + '_' + str(random_uuid) + '.' + file_extension
    data = BytesIO(file_data)

    # Put the object into service
    client.put_object(
        bucket_name=os.environ['MINIO_BUCKET'],
        object_name=file_name,
        length=length,
        data=data
    )
    url = client.get_presigned_url(
        "GET",
        os.environ['MINIO_BUCKET'],
        file_name,
        expires=timedelta(days=7),
    )

    return url
