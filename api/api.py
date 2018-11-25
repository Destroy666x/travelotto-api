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


class GameInvitationViewSet(viewsets.ModelViewSet):
    queryset = GameInvitation.objects.all()
    serializer_class = GameInvitationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LotteryViewSet(viewsets.ModelViewSet):
    queryset = Lottery.objects.all()
    serializer_class = LotterySerializer
