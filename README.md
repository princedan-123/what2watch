# what2watch

## 🎥 Movie Recommendation API

A FastAPI-based backend service that provides movie and TV show recommendations, trending titles, and detailed metadata using The Movie Database (TMDb)

🚀 Features

✅ Fetch popular, trending, upcoming, and top-rated movies and TV shows
✅ Get detailed information about a movie or show (cast, trailers)
✅ Search for movies, TV shows.
✅ Built with FastAPI and async HTTP requests using httpx for high performance

### Install requirements

pip install -r requirements.txt

## Pull Docker image from docker hub

```
sudo docker pull danmab/what2watch:v1
```

## Run docker container

```
sudo docker run -it danmab/what2watch:v1 sh

```

```
touch .env
```

```
echo 'TMDB_API_KEY=API_KEY' > .env
```

```
./start_app
```

### Access the API Docs

Once running, visit:

[Swagger UI →](https://what2watch-1gh0.onrender.com/docs)

[ReDoc →](https://what2watch-1gh0.onrender.com/redoc)

```

```
