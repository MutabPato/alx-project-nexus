from django.db import models
import uuid
from users.models import User

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tmdb_id = models.IntegerField(unique=True) # External TMDB reference
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.title

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        ordering = ['-added_at']
        unique_together = ('user', 'movie') # Prevent duplicate favorites

    def __str__(self):
        return f"{self.movie.title} favorited by {self.user.email}"

class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="recommended_to")
    explanation = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
        unique_together = ('user', 'movie') # Optional: only 1 recommendation per movie/user
