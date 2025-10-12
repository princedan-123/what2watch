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
        return response.json()