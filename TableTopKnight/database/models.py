from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField


# Create your models here.

# User Table
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    email = models.EmailField(max_length=100)
    friends = models.ManyToManyField('User')
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

    def addFriend(self, friend):
        if isinstance(friend, Profile):
            self.friends.add(friend)
            return True
        else:
            return False

    def removeFriend(self, friend):
        if isinstance(friend, Profile):
            self.friends.remove(friend)
            return True
        else:
            return False
    
    def getLibrary(self):
        return library.all()

    def addGame(self, game):
        if isinstance(game, Game):
            self.library.add(game)
            return True
        else:
            return False
    
    def removeGame(self, game):
        if isinstance(game, Game):
            self.library.remove(game)
            return True
        else:
            return False

    def getNotifications(self):
        return self.notifications.all()

    def addNotification(self, message, link):
        Notification.objects.create_notification(
            self.user.id, message, link
        )

# Game Table
class GameManager(models.Manager):
    def getGames(self, gameIDs):
        games = self.filter(gameID__in=gameIDs).all()
        return games
    def create_game(self, gameName, playerMin, playerMax, genre, thmb, desc):
        new_game = self.create(
            gameName = gameName,
            playerMin = playerMin,
            playerMax = playerMax,
            genre = genre,
            thumbnail_url = thmb,
            description = desc
        )
        new_game.save()
        return new_game
    def delete_game(self, gameID):
        self.get(gameID=gameID).delete()


class Game(models.Model):
    gameID = models.AutoField(primary_key=True)
    gameName = models.CharField(max_length=50)
    playerMin = models.IntegerField()
    playerMax = models.IntegerField()
    genre = models.CharField(max_length=50)
    thumbnail_url = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def getGame(self):
        game = {
            "name": self.gameName,
            "minimum_players": self.playerMin,
            "maximum_players": self.playerMax,
            "genre": self.genre,
            "thumbnail": self.thumbnail_url,
            "description": self.description
        }
        return game


# Event Table
class EventManager(models.Manager):
    def create_event(self, host, eventDateTime, location):
        new_event = self.create(
            host=host,
            eventDateTime=eventDateTime,
            location=location
        )
        new_event.save()
        return new_event
    
    def remove_event(self, eventID):
        self.get(eventID=eventID).delete()


class Event(models.Model):
    eventID = models.AutoField(primary_key=True)
    host = models.ForeignKey('User', on_delete=models.CASCADE)
    attendees = models.ManyToManyField("User", related_name="event_attending")
    pendingPlayers = models.ManyToManyField("User", related_name="event_invited")
    eventDateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=200)
    eventGames = models.ManyToManyField("Game")
    objects = EventManager()

    def addPending(self, user):
        if isinstance(user, User):
            self.pendingPlayers.add(user)
            return True
        else:
            return False
    
    def removePending(self, user):
        if isinstance(user, User):
            self.pendingPlayers.remove(user)
            return True
        else:
            return False

    def addAttendee(self, user):
        if isinstance(user, User):
            self.attendees.add(user)
            return True
        else:
            return False
    
    def removeAttendee(self, user):
        if isinstance(user, User):
            self.attendees.remove(user)
            return True
        else:
            return False

    def sendInvites(self):
        for pp in self.pendingPlayers.all():
            pp.profile.addNotification(
                "You've been invited to join an event hosted by "+self.host.profile + ".",
                "insert_url_here"
            )


class NotificationManager(models.Manager):
    def create_notification(self, userID, message, link):
        notif = self.create(recipient_id=userID, message=message, link=link)
        notif.save()
        return notif
    def delete_notification(self, msg):
        msg.delete()

class Notification(models.Model):
    msgID = models.AutoField(primary_key=True)
    recipient = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=200)
    link = models.CharField(max_length=100)
    objects = NotificationManager()