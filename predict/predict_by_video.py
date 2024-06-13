import os
import shutil

import global_context
import image_captioning
from automatic_speech_recognition import speech_recognition

from image_captioning import image_caption as image_captioning
from image_captioning.utils import get_image_hash
from image_captioning.video_to_frames import create_temp_directory_with_frames


def predict(link, description):
    tags = description

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

    speech_text = speech_recognition.recognize_speech(link)
    enrich_result['text'] = speech_text

    embedding_function = global_context.embeddings_service.calc
    enrich_result['text_embedding'] = embedding_function(speech_text)
    enrich_result['description_ru_embedding'] = embedding_function(speech_text)
    enrich_result['tags_embedding'] = embedding_function(tags)
    return enrich_result
