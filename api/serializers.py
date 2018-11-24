from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()


class UserSerializer(serializers.ModelSerializer):
    profile: UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class GameSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Game
        exclude = ()
