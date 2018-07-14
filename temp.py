from datetime import datetime
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    hosts='120.79.91.211'
)

test = es.search(index=['tmp_yikougua1'], doc_type=['douban_movie'], size=2, from_=0)
print(json.dumps(test))

movie_hits = test['hits']['hits']
movies = []
for hit in movie_hits:
    movies.append(hit['_source'])
print(json.dumps(movies))