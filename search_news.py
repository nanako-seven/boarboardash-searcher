from elasticsearch import Elasticsearch
from pydantic import BaseModel
import datetime
from typing import Optional, List
from config import es_host, es_port, index_name

es = Elasticsearch([{"host": es_host, "port": es_port}])

# if (not es.ping()):
#     raise "es not running."


class SearchNewsRequest(BaseModel):
    content: str
    categories: Optional[List[str]]
    date_from: Optional[datetime.date]
    start: int
    end: int


def search_news(q: SearchNewsRequest):
    '''
    根据q构造elasticsearch的请求，返回搜索结果
    '''
    query = {
        'from': q.start,
        'size': q.end - q.start,
        "query": {
            "bool": {
                "must": {
                    "match": {"content": q.content}
                },
                'filter': [],
            }
        },
        "highlight": {
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"],
            "number_of_fragments": 1,
            "fragment_size": 100,
            "fields": {
                "content": {}
            }
        }
    }
    a: list = query['query']['bool']['filter']
    if q.categories:
        a.append({'terms': {'category': q.categories}})
    if q.date_from:
        a.append({'range': {'date': {'gte': q.date_from}}})
    print(q.categories)
    result = es.search(index=index_name, body=query)
    return {'hits': [extract(x) for x in result['hits']['hits']]}


def extract(x):
    '''
    从elasticsearch的返回值中提取需要的信息
    '''
    s = x['_source']
    highlight = x['highlight']['content']
    return {
        'title': s['title'],
        'url': s['url'],
        'highlight': highlight[0] if highlight else '',
    }

# query = NewsQuery(content='test', categories=['category'], date_from=datetime.date(2002, 1, 1), start=0, end=4)
# print(search(query))


class NewsElement(BaseModel):
    content: str
    title: str
    url: str
    category: str
    date: datetime.date


def add_news(e: NewsElement):
    '''
    添加新闻
    '''
    es.index(index=index_name, body=dict(e))
