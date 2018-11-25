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
        point__distance_lt=(Point(point[0], point[1]), Distance(km=data.get('radius', '')))).order_by('?')[:number_of_locations]
    if len(locations_within_radius) < number_of_locations:
        return Response({'error': 'Not enough locations in the area around the chosen point'}, status=status.HTTP_400_BAD_REQUEST)

    questions = []

    for location in locations_within_radius:
        question = LocationQuestion.objects.filter(location=location).order_by('?').first()
        if question is None:
            return Response({'error': 'No question for ' + location.name}, status=status.HTTP_400_BAD_REQUEST)

        questions.append(question)

    try:
        last_lottery = Lottery.objects.latest('create_date')
    except Lottery.DoesNotExist:
        return Response({'error': 'No lottery added'}, status=status.HTTP_400_BAD_REQUEST)

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

    last_lottery.games.add(game)

    serializer = GameSerializer(game)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def visit_location(request, game_id, location_id):
    game = Game.objects.get(pk=game_id)

    expected_location = game.locations.filter(status='TO_VISIT').order_by('order').first()
    current_location = game.locations.get(pk=location_id)

    if current_location.status is None:
        return Response({'error': 'Could not find location'}, status=status.HTTP_400_BAD_REQUEST)

    if current_location.status == 'VISITED_INCORRECTLY':
        return Response({'error': 'This location has already been visited incorrectly'}, status=status.HTTP_400_BAD_REQUEST)

    if expected_location is None:
        return Response({'error': 'No more locations to visit'}, status=status.HTTP_400_BAD_REQUEST)

    if current_location.status == 'TO_VISIT':
        if expected_location == current_location:
            current_location.status = 'VISITED_CORRECTLY'
        else:
            current_location.status = 'VISITED_INCORRECTLY'

        current_location.save()

    question = game.questions.get(question__location=current_location.location)

    if question is None:
        return Response({'error': 'No question for ' + current_location.location.name}, status=status.HTTP_400_BAD_REQUEST)

    if question.status != 'TO_ANSWER':
        return Response({'error': 'Question has already been answered'}, status=status.HTTP_400_BAD_REQUEST)

    answers = [question.question.correct_answer, question.question.incorrect_answer]

    random.shuffle(answers)

    representation = GameQuestionRepresentation()
    representation.question_id = question.id
    representation.question_text = question.question.question_text
    representation.answer_1 = answers[0]
    representation.answer_2 = answers[1]

    return Response(GameQuestionSerializer(representation).data)


@api_view(['POST'])
def answer_question(request, game_id, question_id):
    game = Game.objects.get(pk=game_id)
    question = game.questions.get(pk=question_id)

    if question is None:
        return Response({'error': 'No question found'}, status=status.HTTP_400_BAD_REQUEST)

    if question.status != 'TO_ANSWER':
        return Response({'error': 'Question has already been answered'}, status=status.HTTP_400_BAD_REQUEST)

    answers = [question.question.correct_answer, question.question.incorrect_answer]
    answer = request.data.get('answer')

    if answer not in answers:
        return Response({'error': 'This is not a valid answer. Valid options are: ' + ', '.join(answers)}, status=status.HTTP_400_BAD_REQUEST)

    if answer == question.question.correct_answer:
        question.status = 'ANSWERED_CORRECTLY'
    else:
        question.status = 'ANSWERED_INCORRECTLY'

    question.save()

    return Response({'status': question.status})

@api_view(['GET'])
def get_game_lottery(request, game_id):
    lottery = Lottery.objects.filter(games__id=game_id)[0]

    if lottery is None:
        return Response({'error': 'Invalid game'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = LotterySerializer(lottery)

    return Response(serializer.data, status=status.HTTP_200_OK)


