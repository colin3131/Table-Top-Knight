from django.db import models

# Create your models here.

# User Table
class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    friends = models.ManyToManyField('self')
    notifications = models.CharField(max_length=None)
    library = models.ManyToManyField(Game)

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
    attendees = models.ManyToManyField("Profile")
    eventDateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    eventGames = models.ManyToManyField("Game")

