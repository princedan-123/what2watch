"""Routes for movie endpoints."""
from fastapi import APIRouter
from core.settings import load_env
import httpx

movie_router = APIRouter(prefix='/movie', tags=['movie'])
@movie_router.get('/search')
async def search_movie(query: str, page:int = 1):
    tmdb_key = load_env.TMDB_API_KEY
    print(tmdb_key)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_key}&query={query}&page={page}"
        )
        payload = response.json()
        #  sort search items based on popularity
        payload['results'].sort(key=lambda search_item:search_item['popularity'], reverse=True)
        return payload