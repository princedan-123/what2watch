"""Main app."""
from fastapi import FastAPI
from routers.movie import movie_router
from routers.tv_shows import tv_show_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.include_router(movie_router)
app.include_router(tv_show_router)