from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
import datetime
import random

@api_view(['POST'])
def initialize_game(request):
    data = request.data
    number_of_locations = data.get('number_of_locations', '')

    if number_of_locations < 4 or number_of_locations > 6:
        return Response({'error': 'Invalid number of locations, should be 4-6'}, status=status.HTTP_400_BAD_REQUEST)

    point = data.get('point', '')

    locations_within_radius = Location.objects.filter(
        point__distance_lt=(Point(point[1], point[0]), Distance(km=data.get('radius', ''))))
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


@api_view(['POST'])
def visit_location(request, game_id, location_id):
    game = Game.objects.get(pk=game_id)

    expected_location = game.locations.filter(visited=False).order_by('order').first()
    current_location = game.locations.get(pk=location_id)

    if expected_location is None:
        return Response({'error': 'No more locations to visit'}, status=status.HTTP_400_BAD_REQUEST)

    if expected_location != current_location:
        return Response({'error': 'Incorrect location order'}, status=status.HTTP_400_BAD_REQUEST)

    question = game.questions.get(question__location=current_location.location)

    if question is None:
        return Response({'error': 'No question for ' + current_location.location.name}, status=status.HTTP_400_BAD_REQUEST)

    if question.status != 'TO_ANSWER':
        return Response({'error': 'Question has already been answered'}, status=status.HTTP_400_BAD_REQUEST)

    current_location.visited = True
    current_location.save()

    answers = [question.question.correct_answer, question.question.incorrect_answer]

    random.shuffle(answers)

    representation = GameQuestionRepresentation()
    representation.question_text = question.question.question_text
    representation.answer_1 = answers[0]
    representation.answer_2 = answers[1]

    return Response(GameQuestionSerializer(representation).data)


@api_view(['POST'])
def answer_question(request, game_id, question_id):
    return Response('answer_question, game %d, question %d' % (game_id, question_id))

