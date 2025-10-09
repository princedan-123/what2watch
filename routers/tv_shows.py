"""Router for tv shows."""
from fastapi import APIRouter

tv_show_router = APIRouter(prefix='/tvshow', tags=['tvshows'])