from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import *
from .serializers import *
import datetime
import random


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=False, methods=['POST'])
    def initialize(self, request):
        data = request.data
        number_of_locations = data.get('number_of_locations', '')

        if number_of_locations < 4 or number_of_locations > 6:
            return Response({'error': 'Invalid number of locations, should be 4-6'}, status=status.HTTP_400_BAD_REQUEST)

        point = data.get('point', '')

        locations_within_radius = Location.objects.filter(point__distance_lt=(Point(point[1], point[0]), Distance(km=data.get('radius', ''))))
        if len(locations_within_radius) < number_of_locations:
            return Response({'error': 'Not enough locations in the area around the chosen point'}, status=status.HTTP_400_BAD_REQUEST)

        locations = random.sample(locations_within_radius, number_of_locations)

        questions = []

        for location in locations:
            question = LocationQuestion.objects.filter(location=location).order_by('?').first()
            if question is None:
                return Response({'error': 'No question for ' + location.name}, status=status.HTTP_400_BAD_REQUEST)

            questions.append(question)

        user = User.objects.get(pk=data.get('user_id', ''))

        game = Game.objects.create(
            create_date=datetime.datetime.now(),
            owner=user,
            users=[user],
            locations=locations,
            questions=questions
        )

        serializer = GameSerializer(game)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class GameLocationViewSet(viewsets.ModelViewSet):
    queryset = GameLocation.objects.all()
    serializer_class = GameLocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationQuestionViewSet(viewsets.ModelViewSet):
    queryset = LocationQuestion.objects.all()
    serializer_class = LocationQuestionSerializer


class GameQuestionViewSet(viewsets.ModelViewSet):
    queryset = GameQuestion.objects.all()
    serializer_class = GameQuestionSerializer
