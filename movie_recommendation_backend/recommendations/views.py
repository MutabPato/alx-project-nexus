from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Movie, Favorite, Recommendation
from .serializers import MovieSerializer, FavoriteSerializer, RecommendationSerializer
from rest_framework.response import Response
from .utils.cache import sync_popular_movies, recommend_based_on_favorites
from django.core.cache import cache


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        movies = sync_popular_movies()
        serialzer = MovieSerializer(movies, many=True)
        return Response(serialzer.data)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete(f"user:{self.request.user.id}:recomendations")

class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user).order_by('movie__rating')
    
    def list(self, request, *args, **kwargs):
        recommendations = recommend_based_on_favorites(self.request.user)
        serialzer = self.get_serializer(recommendations, many=True)
        return Response(serialzer.data)

