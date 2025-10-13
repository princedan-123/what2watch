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

@tv_show_router.get('/clips/{tv_id}')
async def clips(tv_id:int):
    """An endpoint that returns information about a tvshow video clips."""
    async with httpx.AsyncClient() as client:
        base_url = f'https://api.themoviedb.org/3/tv/{tv_id}/videos'
        query_parameter = f'?api_key={tmdb_key}'
        response = await client.get(f'{base_url}{query_parameter}')
        response = response.json()['results']
        filtered_response = [
            item for item in response if item['site'] == 'YouTube'
            ]
        #  Generate youtuble links for videos
        videos = [
            {
                'name': video['name'],
                'type': video['type'],
                'published_at': video['published_at'],
                'language': video['iso_639_1'],
                'country': video['iso_3166_1'],
                'official': video['official'],
                'link': f'https://www.youtube.com/watch?v={video['key']}'
            } for video in filtered_response
            ]
        return videos

@tv_show_router.get('/shows_like/{tv_id}', status_code=200)
async def shows_like(tv_id:int, page:int =1):
    """An endpoint that recommends tv shows like the current show."""
    base_url = f'https://api.themoviedb.org/3/tv/{tv_id}/recommendations'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(
                status_code=500, detail='Invalid id: The pre-requisite id is invalid or not found.'
                )
        return response.json()

@tv_show_router.get('/cast_and_crew/{tv_id}', status_code=200)
async def cast_and_crew(tv_id:int):
    """An endpoint that returns cast and crew of a tv show."""
    base_url = f'https://api.themoviedb.org/3/tv/{tv_id}/credits'
    query_parameter = f'?api_key={tmdb_key}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('cast'):
            raise HTTPException(
                status_code=500, detail='Invalid id: The pre-requisite id is invalid or not found.'
                )
        return response.json()

@tv_show_router.get('/popular', status_code=200)
async def popular_tvshows(page:int =1):
    """An endpoints that returns a list of popular tvseries."""
    base_url = f'https://api.themoviedb.org/3/tv/popular'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(status_code=500, detail='server error')
        return response.json()

@tv_show_router.get('/airing_today/', status_code=200)
async def airing_today(page:int = 1):
    """
        An endpoint that returns a list of tv shows airing today
    """
    base_url = f'https://api.themoviedb.org/3/tv/airing_today'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(status_code=500, detail='server error')
        return response.json()