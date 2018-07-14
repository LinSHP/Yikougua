from flask import Flask
from flask_restful import Resource, Api, reqparse
from elasticsearch import Elasticsearch
import config

app = Flask(__name__)
api = Api(app)
es = Elasticsearch(
    hosts=config.es_host
)


class TextSearch(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('text', required=True, help='text must be specified')
        self.parser.add_argument('limit', type=int, default=20)
        self.parser.add_argument('offset', type=int, default=0)

    def get(self):
        args = self.parser.parse_args()
        body = {
            "query": {"query_string": {"query": args['text']}}
        }
        hits = es.search(index=[config.es_index], doc_type=[config.es_type],
                         size=args['limit'], from_=args['offset'], body=body)
        hits = hits['hits']['hits']
        movies = []
        for hit in hits:
            movies.append(hit['_source'])
        return movies, 200


api.add_resource(TextSearch, '/search')

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
