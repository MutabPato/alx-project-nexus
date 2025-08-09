from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from ..models import User

class UserRegistrationTest(APITestCase):
    def test_user_can_register(self):
        url = reverse('users-list') # points to POST /api/users/
        data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "phone_number": "+254712345678",
            "password": "StrongPass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, "test@example.com")


class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="auth@example.com",
            password="StrongPass123",
            first_name="Auth",
            last_name="User",
            username="authuser",
            phone_number="+254712345678"
        )
    
    def test_user_can_login_and_get_token(self):
        url = reverse('token_obtainPair')
        data = {
            "email": "auth@example.com",
            "password": "StrongPass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    