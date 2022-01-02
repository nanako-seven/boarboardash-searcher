from elasticsearch import Elasticsearch
from pydantic import BaseModel
import datetime
from config import es_host, es_port, index_name

es = Elasticsearch([{"host": es_host, "port": es_port}])

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

es.indices.create(index=index_name, body=news_mappings)
