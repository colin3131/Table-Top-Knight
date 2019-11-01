from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField


# Create your models here.

# User Table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    friends = models.ManyToManyField('self')
    notifications = ArrayField(
        JSONField()
    )
    library = models.ManyToManyField("Game")

    def __str__(self):
        return self.user.username

    def verifyLogin(self, _username, _password):
        _user = authenticate(_username, _password)
        if _user is not None:
            return True
        else:
            return False

    def changePassword(self, oldPass, newPass):
        _user = authenticate(self.user.username, oldPass)
        if _user is not None:
            self.user.set_password(newPass)
            return True
        else:
            return False
    
    def getFriends(self):
        return self.friends.all()
        

# Game Table
class Game(models.Model):
    gameName = models.CharField(max_length=50)
    playerMin = models.IntegerField()
    playerMax = models.IntegerField()
    genre = models.CharField(max_length=50)
    thumbnail_url = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

# Event Table
class Event(models.Model):
    host = models.ForeignKey('Profile', on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Profile", related_name="event_hosting")
    eventDateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    eventGames = models.ManyToManyField("Game")