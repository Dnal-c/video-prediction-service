from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from fastapi import APIRouter, HTTPException, Response, UploadFile, status, File, Header, Body, Depends, Form

link_validator = URLValidator()


def predictions_to_response(predictions: dict):
    predictions['tags_vector'] = str(predictions['tags_vector'])
    predictions['voice_vector'] = str(predictions['voice_vector'])
    predictions['description_ru_vector'] = str(predictions['description_ru_vector'])
    return predictions


def validate_link(link):
    try:
        link_validator(link)
        print("String is a valid URL")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ссылка некоректна'
        )
