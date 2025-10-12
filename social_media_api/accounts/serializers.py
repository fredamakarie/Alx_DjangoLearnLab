from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token']

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        # Use create_user() to properly hash the password and handle user setup
        user = get_user_model().objects.create_user(
        username=validated_data.get('username'),
        email=validated_data.get('email'),
        password=validated_data.get('password'),
        bio=validated_data.get('bio', ''),
        profile_picture=validated_data.get('profile_picture', None),
        )

        # Create token for the user after saving
        Token.objects.get_or_create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        token, created = Token.objects.get_or_create(user=user)
        
        return {
            'user_id': user.id,
            'username': user.username,
            'token': token.key
        }