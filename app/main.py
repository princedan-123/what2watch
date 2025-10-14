"""Main app."""
from fastapi import FastAPI
from routers.movie import movie_router
from routers.tv_shows import tv_show_router

app = FastAPI()

app.include_router(movie_router)
app.include_router(tv_show_router)