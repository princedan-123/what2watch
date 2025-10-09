"""Main app."""
from fastapi import FastAPI
from routers.movie import movie_router

app = FastAPI()

app.include_router(movie_router)