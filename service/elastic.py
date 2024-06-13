import os

from elasticsearch import Elasticsearch


class ElasticService:

    def __init__(self):
        host = os.environ['ELASTIC_HOST']
        login = os.environ['ELASTIC_LOGIN']
        password = os.environ['ELASTIC_PASSWORD']
        print(f'ElasticService host: {host}')
        self.es = Elasticsearch(host, basic_auth=(login, password))
        self.index = 'video-index-3'

    def save_prediction(self, data: dict):
        video = {
            'description_ru': data['description_ru'],
            'description_ru_vector': data['description_ru_embedding'],
            'link': data['link'],
            'voice_vector': str(data['text_embedding'] or ''),
            'tags_vector': str(data['tags_embedding'] or ''),
            'tags': str(data['tags'] or None),
            'voice': str(data['text'] or None),
            'summary': str(data['short_description_ru'] or None)
        }

        self.es.index(index=self.index, body=video)
