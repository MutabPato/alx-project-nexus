from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from recommendations.models import Movie, Favorite, Recommendation
from unittest.mock import patch
import uuid


class RecommendationListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="rec@example.com",
            password="pass1234",
            first_name="Rec",
            last_name="User",
            username="recuser",
            phone_number="+254787654321"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.movie = Movie.objects.create(
            tmdb_id=23456,
            title="Original",
            description="Desc",
            rating=9.0
        )
        Favorite.objects.create(user=self.user, movie=self.movie)

    @patch("recommendations.utils.cache.fetch_recommendations_by_movie")
    def test_generate_recommendations(self, mock_fetch):
        mock_fetch.return_value = [
            {
                "id": 34567,
                "title": "Similar Movie",
                "overview": "Similar description",
                "release_date": "2022-10-10",
                "vote_average": 7.5,
                "poster_path": "/similar.png"
            }
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(reverse('recommendations-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['movie'], Movie.objects.get(tmdb_id=34567).id)
