from django.db import models
import uuid
from users.models import User

class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tmbd_id = models.IntegerField(unique=True) # External TMDB reference
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    ratings = models.FloatField(null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie') # Prevent duplicate favorites

class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="recommended_to")
    explanation = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie') # Optional: only 1 recommendation per movie/user
