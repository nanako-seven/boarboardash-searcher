from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from search_news import add_news, search_news, SearchNewsRequest, NewsElement
from search_images import SearchImagesRequest
from datetime import datetime
import base64
import aiohttp
import aiofiles
import random
from models import Image
from image_hash import get_image_hash
import numpy as np
from typing import List, Tuple

app = FastAPI()

origins = [
    '*'
]

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/search-news')
async def search_api(req: Request):
    '''
    搜索新闻的API，请求是SearchNewsRequest
    '''
    json = await req.json()
    return search_news(SearchNewsRequest(**json))


async def get_similarities(src: np.ndarray) -> List[Tuple[str, float]]:
    images = await Image.objects.all()
    return [(x.url, np.dot(src, np.loads(x.hash))) for x in images]


@app.post('/search-images')
async def search_images_api(req: Request):
    '''
    搜索图片的API，请求是SearchImagesRequest
    '''
    json = await req.json()
    r = SearchImagesRequest(**json)
    data = base64.b64decode(r.data)
    n = random.randint(0, 1000000)
    path = f'temp/{n}'
    async with aiofiles.open(path, 'wb') as f:
        await f.write(data)
    h = get_image_hash(path)
    s = await get_similarities(h)
    s.sort(key=lambda x: x[1], reverse=True)
    max_n = json['max_num_hits']
    return {
        'hits': [x[0] for x in s[:max_n]]
    }


@app.post('/_internal/add-news')
async def add_news_api(req: Request):
    '''
    添加新闻的API，不对外公开
    '''
    json = await req.json()
    json['date'] = datetime.strptime(json['date'], '%Y-%m-%d').date()
    e = NewsElement(content=json['content'], title=json['title'],
                    url=json['url'], category=json['category'], date=json['date'])
    add_news(e)
    return {'status': 'ok'}


async def download(url, path):
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        if r.status != 200:
            raise RuntimeError('下载图片失败')
        async with aiofiles.open(path, 'wb') as f:
            await f.write(await r.read())


@app.post('/_internal/add-image')
async def add_image_api(req: Request):
    '''
    添加图片的API，不对外公开
    '''
    json = await req.json()
    n = random.randint(0, 1000000)
    ext = json['url'].split('.')[-1]
    download_path = f'temp/{n}.{ext}'
    await download(json['url'], download_path)
    h = get_image_hash(download_path).dumps()
    await Image.objects.create(url=json['url'], hash=h)
    return {'status': 'ok'}
