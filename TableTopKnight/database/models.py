from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

# User Table
# HOW TO ACCESS PROFILE: user.profile
# HOW TO ACCESS PROFILE ATTRIBS: user.profile.library, user.profile.friends
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    friends = models.ManyToManyField('self')
    library = models.ManyToManyField("Game")

    def __str__(self):
        return self.user.username

    # Verifies the login of an individual user
    def verifyLogin(self, _username, _password):
        _user = authenticate(_username, _password)
        if _user is not None:
            return True
        else:
            return False

    # Changes the password of an individual user supplied old and new pass
    def changePassword(self, oldPass, newPass):
        _user = authenticate(self.user.username, oldPass)
        if _user is not None:
            self.user.set_password(newPass)
            return True
        else:
            return False
    
    # Returns the Profile of all friends
    # user.profile.getFriends()
    def getFriends(self):
        return self.friends.all()

    # Adds a friend to the profile
    # user.profile.addFriend(Profile instance)
    def addFriend(self, friend):
        if isinstance(friend, Profile):
            self.friends.add(friend)
            return True
        else:
            return False

    # Removes a friend from the profile
    # user.profile.removeFriend(Profile instance)
    def removeFriend(self, friend):
        if isinstance(friend, Profile):
            self.friends.remove(friend)
            return True
        else:
            return False
    
    # Returns the library of the user
    # user.profile.getLibrary()
    def getLibrary(self):
        return library.all()

    # Adds a game to a user's library
    # user.profile.addGame(Game instance)
    def addGame(self, game):
        if isinstance(game, Game):
            self.library.add(game)
            return True
        else:
            return False
    
    # Removes a game from the user's library
    # user.profile.removeGame(Game instance)
    def removeGame(self, game):
        if isinstance(game, Game):
            self.library.remove(game)
            return True
        else:
            return False

    # Returns all of the notifications belonging to a user
    # user.profile.getNotifications()
    def getNotifications(self):
        return self.notifications.all()

    # Adds a notification to a user
    # user.profile.addNotification(string:message, string:link)
    def addNotification(self, message, link):
        Notification.objects.create_notification(
            self.user.id, message, link
        )

    # Removes a notification from a user
    # user.profile.removeNotification(Notification instance)
    def removeNotification(self, notification):
        if isinstance(notification, Notification):
            self.notifications.remove(notification)
            return True
        else:
            return False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Game Table
class GameManager(models.Manager):
    def getGames(self, gameIDs):
        games = self.filter(gameID__in=self.id).all()
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
        self.get(gameID=self.id).delete()


class Game(models.Model):
    gameName = models.CharField(max_length=50, default="")
    playerMin = models.IntegerField()
    playerMax = models.IntegerField()
    genre = models.CharField(max_length=50, default="")
    thumbnail_url = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=200, default="")

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
        self.get(eventID=self.id).delete()


class Event(models.Model):
    host = models.ForeignKey('profile', on_delete=models.CASCADE)
    attendees = models.ManyToManyField("profile", related_name="event_attending")
    pendingPlayers = models.ManyToManyField("profile", related_name="event_invited")
    eventDateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=200, default="The Basement")
    eventGames = models.ManyToManyField("Game")
    objects = EventManager()
    PRE_VOTING = 'PV'
    VOTING = 'VO'
    AFTER_VOTING = 'AV'
    EVENT_STATES = [
        (PRE_VOTING, 'Event Setup Phase'),
        (VOTING, 'Voting Phase'),
        (AFTER_VOTING, 'Post-Voting Phase'),
    ]
    event_state = models.CharField(
        max_length=2,
        choices=EVENT_STATES,
        default=PRE_VOTING
    )

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
                "You've been invited to join an event hosted by " + self.host.profile + ".",
                "insert_url_here"
            )

    # Check if the event currently allows voting
    # event.canVote() returns true/false
    def canVote(self):
        return self.event_state in self.VOTING

    # Check if the event currently allows inviting new players
    # event.canInvite() returns true/false
    def canInvite(self):
        return self.event_state in self.PRE_VOTING

    # Check if the event is ready to play the game
    # event.canPlay() returns true/false
    def canPlay(self):
        return self.event_state in self.AFTER_VOTING

    # Set the event to the Voting phase
    # event.startVoting()
    def startVoting(self):
        self.event_state = self.VOTING

    # End the event's voting phase
    # event.endVoting()
    def endVoting(self):
        self.event_state = self.AFTER_VOTING

class NotificationManager(models.Manager):
    def create_notification(self, userID, message, link):
        notif = self.create(recipient_id=userID, message=message, link=link)
        notif.save()
        return notif
    def delete_notification(self, msg):
        msg.delete()

class Notification(models.Model):
    recipient = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=100, default="")
    objects = NotificationManager()