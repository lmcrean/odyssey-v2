# users/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'date_joined', 'updated_at')
        read_only_fields = ('id', 'date_joined', 'updated_at')


class UserRegistrationSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)