"""
URL configuration for movie_recommendation_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from recommendations.views import MovieViewSet, FavoriteViewSet, RecommendationViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'movies', MovieViewSet, basename='movies')
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'recommendations', RecommendationViewSet, basename='recommendations')

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Recommendation API",
        default_version='v1',
        description="API for recommending movies based on user favorites.",
        contact=openapi.Contact(email="patrick.m.mutabazi@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # App routes
    path('api/', include(router.urls)),

    # Auth (JWT) routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtainPair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger UI at /api/docs/
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # ReDoc UI at /api/redoc/
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Raw JSON and YAML schema (for dev tools or testing)
    path('api/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

]
