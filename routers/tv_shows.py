"""Router for tv shows."""
from fastapi import APIRouter, HTTPException
from core.settings import load_env
import httpx

tmdb_key = load_env.TMDB_API_KEY
tv_show_router = APIRouter(prefix='/tvshow', tags=['tvshows'])
@tv_show_router.get('/search', status_code=200)
async def search_tvshow(query: str, page:int = 1):
    async with httpx.AsyncClient() as client:
        base_url = 'https://api.themoviedb.org/3/search/tv'
        query_parameter = f'?api_key={tmdb_key}&query={query}&page={page}'
        response = await client.get(f'{base_url}{query_parameter}')
        payload = response.json()
        if len(payload['results']) == 0:
            raise HTTPException(status_code=404, detail='No match found!!')
        #  sort search items based on popularity
        payload['results'].sort(key=lambda search_item:search_item['popularity'], reverse=True)
        return payload

@tv_show_router.get('/get/{tv_id}', status_code=200)
async def get_tvshow(tv_id:int):
    """An endpoint that fetches a specific tvshow."""
    async with httpx.AsyncClient() as client:
        base_url = 'https://api.themoviedb.org/3/tv/'
        response = await client.get(f'{base_url}{tv_id}?api_key={tmdb_key}')
        if not response.json():
            raise HTTPException(
                status_code=500, detail='Oops an error occured!!'
                )
        return response.json()
