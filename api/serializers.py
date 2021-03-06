from rest_framework import serializers
from .models import *
from .fields import LocationField


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()
        depth = 2


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LocationSerializer(serializers.ModelSerializer):
    point = LocationField()

    class Meta:
        model = Location
        fields = ('id', 'name', 'description', 'point', 'photo')


class CouponSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Coupon
        exclude = ()


class GameLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = GameLocation
        fields = ('id', 'status', 'location', 'order')


class GameQuestionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    question_text = serializers.CharField(max_length=200)
    answer_1 = serializers.CharField(max_length=200)
    answer_2 = serializers.CharField(max_length=200)


class GameSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)
    owner = UserSerializer()
    locations = GameLocationSerializer(many=True)
    wonCoupon = CouponSerializer()

    class Meta:
        model = Game
        exclude = ('questions',)


class GameInvitationSerializer(serializers.ModelSerializer):
    game = GameSerializer()
    recipient = UserSerializer()
    sender = UserSerializer()

    class Meta:
        model = GameInvitation
        exclude = ()


class LotterySerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True)

    class Meta:
        model = Lottery
        exclude = ()


UserProfileSerializer.active_game = GameSerializer
UserProfileSerializer.won_lotteries = LotterySerializer(many=True)
