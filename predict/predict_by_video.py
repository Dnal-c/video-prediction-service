import os
import shutil

import global_context
import image_captioning
from automatic_speech_recognition import speech_recognition

from image_captioning import image_caption as image_captioning
from image_captioning.utils import get_image_hash
from image_captioning.video_to_frames import create_temp_directory_with_frames


def predict(link, description):
    tags = description if description is not None else ''

    enrich_result = {
        'link': link,
        'tags': tags
    }

    directory_name = create_temp_directory_with_frames(link)

    first_file_name = os.path.join(directory_name, 'frame_1.jpg')
    video_hash = get_image_hash(first_file_name)
    enrich_result['hash'] = str(video_hash)

    image_captioning_result = image_captioning.get_video_caption(directory_name,
                                                                 model=global_context.image_captioner,
                                                                 image_processor=global_context.image_processor,
                                                                 tokenizer=global_context.image_tokenizer)
    enrich_result.update(image_captioning_result)
    shutil.rmtree(directory_name)

    speech_result = speech_recognition.recognize_speech(link)
    speech_text = speech_result if speech_result is not None else ''
    enrich_result['voice_text'] = speech_text

    embedding_function = global_context.embeddings_service.calc

    voice_vector = embedding_function(speech_text)
    enrich_result['voice_vector'] = voice_vector

    description_ru = image_captioning_result['description_ru']
    description_ru_vector = embedding_function(description_ru)
    enrich_result['description_ru_vector'] = description_ru_vector

    tags_vector = embedding_function(tags)
    enrich_result['tags_vector'] = tags_vector
    return enrich_result
