from rest_framework import viewsets
from .models import *
from .serializers import *

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


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
