import os

import numpy as np
from elasticsearch import Elasticsearch


class ElasticService:

    def __init__(self):
        host = os.environ['ELASTIC_HOST']
        login = os.environ['ELASTIC_LOGIN']
        password = os.environ['ELASTIC_PASSWORD']
        print(f'ElasticService host: {host}')
        self.es = Elasticsearch(host, basic_auth=(login, password))
        self.index = 'video-index'

    def save_prediction(self, data: dict):
        description_vector = data['description_ru_vector'] if data['description_ru_vector'] is not None else  np.array([])
        voice_vector = data['voice_vector'] if data['voice_vector'] is not None else np.array([])
        tags_vector = data['tags_vector'] if data['tags_vector'] is not None else np.array([])
        video = {
            'description_ru': data['description_ru'],
            'link': data['link'],
            'tags': str(data['tags'] or None),
            'voice': str(data['voice_text'] or None),
            'description_ru_vector': description_vector,
            'voice_vector': voice_vector,
            'tags_vector': tags_vector,
            'summary': str(data['short_description_ru'] or None)
        }

        self.es.index(index=self.index, body=video)
