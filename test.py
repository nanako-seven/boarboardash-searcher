from elasticsearch import Elasticsearch
from pydantic import BaseModel
import datetime

es = Elasticsearch([{"host": "localhost", "port": 9200}])

if (not es.ping()):
    raise "es not running."

# 需要安装analysis-icu，在/bin目录下运行elasticsearch-plugin install analysis-icu

news_mappings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "cjk_analyzer": {
                        "type": "custom",
                        "tokenizer" : "icu_tokenizer"
                    }
                }
            }
        }
    },
    "mappings" : {
        "properties": {
            # 网页内容
            "content": {
                "type": "text",
                'analyzer': 'cjk_analyzer',
            },
            # 网页标题
            "title": {
                "type": "text",
                'analyzer': 'cjk_analyzer',
            },
            # 网页url
            "url": {
                "type": "keyword",
            },
            # 网页种类
            'category': {
                'type': 'text',
                'analyzer': 'whitespace',
            },
            # 新闻发布时间
            'date': {
                'type': 'date',
            }
        }
    }
}

es.indices.create(index='news-index', body=news_mappings)

class NewsElement(BaseModel):
    content: str
    title: str
    url: str
    category: str
    date: datetime.date

elem = dict(NewsElement(content="test content", title='test title', url='http://example.com', category='test category', date=datetime.date(2002, 1, 1)))

es.index(index="news-index", body=elem)
