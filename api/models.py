from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point

from .enums import GameQuestionStatus


class Location(models.Model):
    point = PointField(default=Point(x=18.66, y=50.29))
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

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
        max_length=20,
        choices=GameQuestionStatus.choices(),
        default=GameQuestionStatus.TO_ANSWER
    )

    def __str__(self):
        return self.question.__str__()


class GameLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    visited = models.BooleanField(default=False)
    order = models.SmallIntegerField()
    # question = models.ForeignKey(LocationQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.location.name + ' ' + self.location.description


class Coupon(models.Model):
    code = models.CharField(max_length=40)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    tier = models.SmallIntegerField


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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name="active_game")
    games = models.ManyToManyField(Game, related_name="games")
    invitations = models.ForeignKey(GameInvitation, on_delete=models.CASCADE, null=True, blank=True)


class GameQuestionRepresentation:
    question_text = ''
    answer_1 = ''
    answer_2 = ''
