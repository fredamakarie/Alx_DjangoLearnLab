from models import Followers, CustomUser
from rest_framework import serializers


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    followers = FollowerSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'