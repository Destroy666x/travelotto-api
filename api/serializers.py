from rest_framework import serializers
from .models import *


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        exclude = ()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ()
        # exclude = ('password',)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()
