from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'password']

    def create(self, validated_data):
        # Remove password from validated_data so that we can use set_password
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) # Hash password and store it securely
        user.save()
        return user
    
    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        verbose_name = "User"
        verbose_name_plural = "Users"
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number']

    
