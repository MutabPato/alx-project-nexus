from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from users.models import User
from recommendations.models import Movie, Favorite


class FavoriteListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="fav@example.com",
            password="pass1234",
            first_name="Fav",
            last_name="User",
            username="favuser",
            phone_number="+254755667788"
        )
        
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        self.movie = Movie.objects.create(
            tmdb_id=12345,
            title="Example Movie",
            description="Nice",
            rating=8.5
        )

    def test_add_favorite(self):
        url = reverse('favorites-list')
        data = {
            'movie': str(self.movie.id),
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Favorite.objects.count(), 1)
