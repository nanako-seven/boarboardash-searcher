from fastapi import FastAPI, Request
from search import add, search, NewsQuery, NewsElement
from datetime import datetime

app = FastAPI()

@app.post('/search-news')
async def search_api(req: Request):
    json = await req.json()
    return search(NewsQuery(**json))

@app.post('/_internal/add-news')
async def add_api(req: Request):
    json = await req.json()
    json['date'] = datetime.strptime(json['date'], '%Y-%m-%d').date()
    e = NewsElement(content=json['content'], title=json['title'], url=json['url'], category=json['category'], date=json['date'])
    add(e)
    return {'status': 'ok'}