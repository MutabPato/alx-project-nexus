from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class MovieListTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="movieuser@example.com",
            password="pass123",
            first_name="Movie",
            last_name="User",
            username="movieuser",
            phone_number="+254711223344"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_list_movies_autheticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer' + self.token)
        response = self.client.get(reverse('movies-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_list_movies_unauthenticated(self):
        response = self.client.get(reverse('movies-list'))
        self.assertEqual(response.status_code, 200)
