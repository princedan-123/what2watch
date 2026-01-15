"""Routes for movie endpoints."""
from fastapi import APIRouter, HTTPException
from core.settings import load_env
import httpx

tmdb_key = load_env.TMDB_API_KEY
movie_router = APIRouter(prefix='/movie', tags=['movie'])
@movie_router.get('/search', status_code=200)
async def search_movie(query: str, page:int = 1) -> dict:
    """
    An endpoint that uses key words to search for movies.
    Return: returns a list of movies that matches the search keyword.
    """
    
    async with httpx.AsyncClient() as client:
        base_url = 'https://api.themoviedb.org/3/search/movie'
        query_parameter = f'?api_key={tmdb_key}&query={query}&page={page}'
        response = await client.get(f'{base_url}{query_parameter}')
        payload = response.json()
        if len(payload['results']) == 0:
            raise HTTPException(status_code=404, detail='No match found!!')
        #  sort search items based on popularity
        payload['results'].sort(key=lambda search_item:search_item['popularity'], reverse=True)
        return payload

@movie_router.get('/get/{movie_id}')
async def get_movie(movie_id:int):
    """An endpoint that fetches a specific movie."""
    async with httpx.AsyncClient() as client:
        base_url = 'https://api.themoviedb.org/3/movie/'
        response = await client.get(f'{base_url}{movie_id}?api_key={tmdb_key}')
        if not response.json():
            raise HTTPException(
                status_code=500, detail='Oops an error occured!!'
                )
        return response.json()

@movie_router.get('/clips/{movie_id}')
async def clips(movie_id:int):
    """An endpoint that returns information about a movie video clips."""
    async with httpx.AsyncClient() as client:
        base_url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos'
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
                'link': f'https://www.youtube.com/embed/{video['key']}'
            } for video in filtered_response
            ]
        return videos

@movie_router.get('/movies_like/{movie_id}', status_code=200)
async def movies_like(movie_id:int, page:int =1):
    """An endpoint that recommends movies like the current movies."""
    base_url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(
                status_code=500, detail='Invalid id: The pre-requisite id is invalid or not found.'
                )
        return response.json()

@movie_router.get('/cast_and_crew/{movie_id}', status_code=200)
async def cast_and_crew(movie_id:int):
    """An endpoint that returns cast and crew of a movie."""
    base_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    query_parameter = f'?api_key={tmdb_key}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('cast'):
            raise HTTPException(
                status_code=500, detail='Invalid id: The pre-requisite id is invalid or not found.'
                )
        return response.json()

@movie_router.get('/popular', status_code=200)
async def popular_movies(page:int =1):
    """An endpoints that returns a list of popular movies."""
    base_url = f'https://api.themoviedb.org/3/movie/popular'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(status_code=500, detail='server error')
        return response.json()

@movie_router.get('/trending/{duration}', status_code=200)
async def trending_movies(duration:str = 'day', page:int = 1):
    """An endpoints that returns a list of trending movies."""
    if duration not in ['week', 'day']:
        raise HTTPException(status_code=400, detail='Invalid trend duration')
    base_url = f'https://api.themoviedb.org/3/trending/movie/{duration}'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(status_code=500, detail='server error')
        return response.json()

@movie_router.get('/now_playing/', status_code=200)
async def now_playing(page:int = 1):
    """
        An endpoints that returns a list of movies currently
        playing in theatres.
    """
    base_url = f'https://api.themoviedb.org/3/movie/now_playing'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(status_code=500, detail='server error')
        return response.json()

@movie_router.get('/upcoming/', status_code=200)
async def upcoming_movies(page:int = 1):
    """
        An endpoint that returns a list of upcoming movies
    """
    base_url = f'https://api.themoviedb.org/3/movie/upcoming'
    query_parameter = f'?api_key={tmdb_key}&page={page}'
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{base_url}{query_parameter}')
        if not response.json().get('results'):
            raise HTTPException(status_code=500, detail='server error')
        return response.json()