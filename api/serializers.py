from rest_framework import serializers
from .models import *
from .fields import LocationField


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()


class UserSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LocationQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationQuestion
        fields = ('question_text', 'correct_answer', 'incorrect_answer', 'location')


class LocationSerializer(serializers.ModelSerializer):
    point = LocationField()

    class Meta:
        model = Location
        fields = ('id', 'name', 'description', 'point')


class GameLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    # question = LocationQuestionSerializer()

    class Meta:
        model = GameLocation
        # fields = ('visited', 'location', 'question')
        fields = ('visited', 'location')


class GameQuestionSerializer(serializers.ModelSerializer):
    question = LocationQuestionSerializer()

    class Meta:
        model = GameQuestion
        fields = ('status', 'question')


class GameSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    owner = UserSerializer()
    locations = GameLocationSerializer(many=True)
    questions = GameQuestionSerializer(many=True)

    class Meta:
        model = Game
        exclude = ()


UserProfileSerializer.active_game = GameSerializer
