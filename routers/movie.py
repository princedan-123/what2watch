"""Routes for movie endpoints."""
from fastapi import APIRouter
from core.settings import load_env
import httpx

movie_router = APIRouter(prefix='/movie', tags=['movie'])
@movie_router.get('/search')
async def search_movie(query: str):
    tmdb_key = load_env.TMDB_API_KEY
    async with httpx.AsyncClient() as client:
        response = await client.get(f"""
        https://api.themoviedb.org/3/search/movie?api_key=tmdb_key&query={query}"""
        )
        return response