from .tmdb import fetch_trending_movies, fetch_recommendations_by_movie
from ..models import Movie, Recommendation, Favorite
from django.db import IntegrityError
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

POPULAR_KEY = "popular_movies:v2"  # bump to invalidate old data
USER_REC_KEY = "user:{user_id}:recommendations:v2"

def sync_popular_movies():
    """
    Cache only the list of tmdb_id's, and always return fresh DB rows.
    """
    ids = cache.get(POPULAR_KEY)
    if ids is not None:
        logger.info("Popular movies cache HIT")
        # Rehydrate from DB so detail view always match list
        movies = list(Movie.objects.filter(tmdb_id__in=ids))
        # Preserve the cached order
        movie_by_tmdb = {m.tmdb_id: m for m in movies}
        return [movie_by_tmdb[i] for i in ids if i in movie_by_tmdb]
    
    logger.info("Popular movies cache MISS")

    tmdb_data = fetch_trending_movies()
    if not tmdb_data:
        logger.warning("TMDB returned no trending movies")
        # Cache empty briefly toavoid hammering TMDB when it's down
        cache.set(POPULAR_KEY, [], timeout=60 * 5)
        return []
    
    ids = []
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

        ids.append(movie.tmdb_id)
    
    cache.set(POPULAR_KEY, ids, timeout=60 * 60) # cache for 1 hour
    return list(Movie.objects.filter(tmdb_id__in=ids))


def recommend_based_on_favorites(user):
    """
    Build recommendations from favorites. Cache only the recommendation IDs.
    Always return fresh DB rows so serializers and detail routes are in sync.
    """
    cache_key = USER_REC_KEY.format(user_id=user.id)
    rec_ids = cache.get(cache_key)

    if rec_ids is not None:
        logger.info(f"Cache HIT for {cache_key}")
        # Rehydrate from DB; keep same order as cached (stable and predictable)
        qs = Recommendation.objects.filter(id__in=rec_ids)
        # preserve order
        rec_map = {str(r.id): r for r in qs}
        return [rec_map[str(i)] for i in rec_ids if str(i) in rec_map]
    
    logger.info(f"Cache MISS for {cache_key}")
    
    favorites = Favorite.objects.filter(user=user).select_related("movie")
    created_recs = []

    for favorite in favorites:
        tmdb_similars = fetch_recommendations_by_movie(favorite.movie.tmdb_id)
        
        for movie_data in tmdb_similars:
            movie, _ = Movie.objects.get_or_create(
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
    if created_recs:
        rec_ids = [str(r.id) for r in created_recs]
        cache.set(cache_key, rec_ids, timeout=60 * 30) # Cache for 30 minutes
        return created_recs
    
    # If nothing new was created, fall back to existing recs from DB
    existing = list(
        Recommendation.objects.filter(user=user).order_by("movie__rating")
    )
    # Cache even empty list briefly to avoid repeated expensive work
    cache.set(cache_key, [str(r.id) for r in existing], timeout=60 * 5)
    return existing
