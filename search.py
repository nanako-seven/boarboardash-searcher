from elasticsearch import Elasticsearch
from pydantic import BaseModel
import datetime
from typing import Optional, List

es = Elasticsearch([{"host": "localhost", "port": 9200}])

if (not es.ping()):
    raise "es not running."
print('ok')

class NewsQuery(BaseModel):
    content: str
    categories: Optional[List[str]]
    date_from: Optional[datetime.date]
    start: int
    end: int


def search(q: NewsQuery):
    query = {
        'from': q.start,
        'size': q.end - q.start,
        "query": {
            "bool" : {
                "must" : {
                    "match" : { "content" : q.content }
                },
                'filter': [],
            }
        },
        "highlight": {
            "pre_tags" : ["<em>"],
            "post_tags" : ["</em>"],
            "number_of_fragments" : 1,
            "fragment_size" : 100,
            "fields": {
                "content": {}
            }
        }
    }
    a: list = query['query']['bool']['filter']
    if q.categories:
        a.append({'terms' : {'category': q.categories}})
    if q.date_from:
        a.append({'range': {'date': {'gte': q.date_from}}})
        

    result = es.search(index="news-index", body=query)
    return {'hits': [extract(x) for x in result['hits']['hits']]}

def extract(x):
    s = x['_source']
    highlight =  x['highlight']['content']
    return {
        'title': s['title'],
        'url': s['url'],
        'highlight': highlight[0] if highlight else '',
    }

# query = NewsQuery(content='test', categories=['category'], date_from=datetime.date(2002, 1, 1), start=0, end=4)
# print(search(query))