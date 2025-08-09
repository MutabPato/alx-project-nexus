from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import UserCreateSerializer, UserReadSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserReadSerializer
        return UserCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()] # Allow user registrtion without login
        return [IsAuthenticated()] # All other actions require authentication
