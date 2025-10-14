"""A module for configuration settings."""
from pydantic_settings import BaseSettings

class LoadEnv(BaseSettings):
    """Environment variables configuration."""
    TMDB_API_KEY:str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8" 

load_env = LoadEnv()
