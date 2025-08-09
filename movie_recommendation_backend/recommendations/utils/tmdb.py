import requests
from django.conf import settings

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = settings.TMDB_BASE_URL

def fetch_trending_movies():
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        return []
    
def fetch_recommendations_by_movie(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        return []