from fastapi import APIRouter

from pydantic import BaseModel

import global_context
from predict import predict_by_video
from controller.common import validate_link, predictions_to_response

router = APIRouter(tags=['Предсказание по видео. Версия для работы с link'])


class LinkRequest(BaseModel):
    link: str
    description: str | None = None


@router.post('/index')
async def predict(request: LinkRequest):
    link = request.link
    validate_link(link)

    tags = request.description

    predictions = predict_by_video.predict(link, tags)
    global_context.elastic_service.save_prediction(predictions)

    return predictions_to_response(predictions)
