from fastapi import FastAPI, Request
from search_news import add_news, search_news, SearchNewsRequest, NewsElement
from search_images import SearchImagesRequest
from datetime import datetime
import base64

app = FastAPI()


@app.post('/search-news')
async def search_api(req: Request):
    json = await req.json()
    return search_news(SearchNewsRequest(**json))


@app.post('/search-images')
async def search_images_api(req: Request):
    json = await req.json()
    r = SearchImagesRequest(**json)
    data = base64.b64decode(r.data)
    with open('out.png', 'wb') as f:
        f.write(data)
    return {'status': 'ok'}


@app.post('/_internal/add-news')
async def add_api(req: Request):
    json = await req.json()
    json['date'] = datetime.strptime(json['date'], '%Y-%m-%d').date()
    e = NewsElement(content=json['content'], title=json['title'],
                    url=json['url'], category=json['category'], date=json['date'])
    add_news(e)
    return {'status': 'ok'}


@app.post('/_internal/add-image')
async def search_api(req: Request):
    json = await req.json()
    return {'status': 'ok'}
