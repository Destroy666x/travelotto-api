from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator
from .enums import GameQuestionStatus, GameLocationStatus


class Location(models.Model):
    point = PointField(default=Point(x=18.66, y=50.29))
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    photo = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class LocationQuestion(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    incorrect_answer = models.CharField(max_length=200)

    def __str__(self):
        return 'Question about %s: %s ("%s" or "%s")' % (self.location.name, self.question_text, self.correct_answer, self.incorrect_answer)


class GameQuestion(models.Model):
    question = models.ForeignKey(LocationQuestion, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        choices=GameQuestionStatus.choices(),
        default=GameQuestionStatus('TO_ANSWER')
    )


class GameLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=GameLocationStatus.choices(),
        default=GameLocationStatus('TO_VISIT')
    )
    order = models.SmallIntegerField()

    def __str__(self):
        return self.location.name


class Coupon(models.Model):
    code = models.CharField(max_length=40)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    tier = models.SmallIntegerField(validators=[MaxValueValidator(4), MinValueValidator(1)], default=2)
    value = models.IntegerField(default=30)


class Game(models.Model):
    create_date = models.DateTimeField('date published')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    users = models.ManyToManyField(User, related_name="users")
    questions = models.ManyToManyField(GameQuestion, related_name="questions")
    locations = models.ManyToManyField(GameLocation, related_name="locations")
    wonCoupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Game #%d' % self.id


class GameInvitation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)


class Lottery(models.Model):
    games = models.ManyToManyField(Game, related_name="lottery_games", blank=True)
    create_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')
    prize = models.BigIntegerField()

    def __str__(self):
        return self.end_date.isoformat(' ', 'seconds')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name="active_game")
    games = models.ManyToManyField(Game, related_name="games")
    won_lotteries = models.ForeignKey(Lottery, on_delete=models.CASCADE, null=True, blank=True)
    invitations = models.ForeignKey(GameInvitation, on_delete=models.CASCADE, null=True, blank=True)


class GameQuestionRepresentation:
    question_id = None
    question_text = ''
    answer_1 = ''
    answer_2 = ''
