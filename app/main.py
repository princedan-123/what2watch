"""Main app."""
from fastapi import FastAPI
from routers.movie import movie_router
from routers.tv_shows import tv_show_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:3000",              # local React / Vite / Next dev
    "http://127.0.0.1:3000",
    "https://what2watch-sandy.vercel.app", # your Vercel frontend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)
app.include_router(movie_router)
app.include_router(tv_show_router)