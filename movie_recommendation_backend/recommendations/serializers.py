from rest_framework import serializers
from .models import Movie, Favorite, Recommendation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'tmbd_id', 'title', 'description', 'release_date',
                  'ratings', 'poster_url']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'movie', 'added_at']

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'movie', 'explanation', 'added_at']