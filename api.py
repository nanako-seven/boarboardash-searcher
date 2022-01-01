from fastapi import FastAPI, Request
from search import search, NewsQuery

app = FastAPI()

@app.get('/search-news')
async def search_api(req: Request):
    json = await req.json()
    return search(NewsQuery(**json))
