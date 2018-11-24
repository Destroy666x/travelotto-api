from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
import datetime

@api_view(['POST'])
def initialize_game(request):
    data = request.data
    number_of_locations = data.get('number_of_locations', '')

    if number_of_locations < 4 or number_of_locations > 6:
        return Response({'error': 'Invalid number of locations, should be 4-6'}, status=status.HTTP_400_BAD_REQUEST)

    point = data.get('point', '')

    locations_within_radius = Location.objects.filter(
        point__distance_lt=(Point(point[0], point[1]), Distance(km=data.get('radius', '')))).order_by('?')[:number_of_locations]
    if len(locations_within_radius) < number_of_locations:
        return Response({'error': 'Not enough locations in the area around the chosen point'}, status=status.HTTP_400_BAD_REQUEST)

    questions = []

    for location in locations_within_radius:
        question = LocationQuestion.objects.filter(location=location).order_by('?').first()
        if question is None:
            return Response({'error': 'No question for ' + location.name}, status=status.HTTP_400_BAD_REQUEST)

        questions.append(question)

    user = User.objects.get(pk=data.get('user_id', ''))

    game = Game.objects.create(
        create_date=datetime.datetime.now(),
        owner=user
    )
    game.users.add(user)

    i = 1

    for location in locations_within_radius:
        game_location = GameLocation.objects.create(
            location=location,
            order=i
        )

        i += 1
        game.locations.add(game_location)

    for question in questions:
        game_question = GameQuestion.objects.create(
            question=question
        )
        game.questions.add(game_question)

    game.save()

    serializer = GameSerializer(game)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
