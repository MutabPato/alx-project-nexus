from .tmdb import fetch_trending_movies, fetch_recommendations_by_movie
from ..models import Movie, Recommendation, Favorite
from django.db import IntegrityError
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def sync_popular_movies():
    cached = cache.get('popular_movies')

    if cached:
        logger.info("Popular movies cache HIT")
        return cached
    else:
        logger.info("Popular movies cache MISS")

    tmdb_data = fetch_trending_movies()
    if not tmdb_data:
        logger.warning("TMDB returned no trending movies")
        return []
    
    movies = []

    for item in tmdb_data:
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=item["id"],
            defaults={
                "title": item["title"],
                "description": item.get("overview", ""),
                "release_date": item.get("release_date", None),
                "rating": item.get("vote_average", 0),
                "poster_url": f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{item.get('poster_path')}"
            }
        )

        movies.append(movie)
    
    # Prevent caching empty movies
    if movies:    
        cache.set('popular_movies', movies, timeout=60 * 60) # cache for 1 hour
    return movies

def recommend_based_on_favorites(user):
    cache_key = f"user:{user.id}:recommendations"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        logger.info(f"Cache HIT for {cache_key}")
        return cached_data
    else:
        logger.info(f"Cache MISS for {cache_key}")
    
    favorites = Favorite.objects.filter(user=user).select_related("movie")
    recommendations = []

    for favorite in favorites:
        tmdb_similars = fetch_recommendations_by_movie(favorite.movie.tmdb_id)
        
        for movie_data in tmdb_similars:
            movie, created = Movie.objects.get_or_create(
            tmdb_id=movie_data["id"],
            defaults={
                "title": movie_data["title"],
                "description": movie_data.get("overview", ""),
                "release_date": movie_data.get("release_date", None),
                "rating": movie_data.get("vote_average", 0),
                "poster_url": f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{movie_data.get('poster_path')}"
            }
        )
            try:
                recommendation, _ = Recommendation.objects.get_or_create(
                    user=user,
                    movie=movie,
                    defaults={"explanation": f"Because you liked {favorite.movie.title}"}
                )
                recommendations.append(recommendation)
            except IntegrityError:
                continue

    # Prevent caching empty recommendations
    if recommendations:
        cache.set(cache_key, recommendations, timeout=60 * 30) # Cache for 30 minutes
    return recommendations
