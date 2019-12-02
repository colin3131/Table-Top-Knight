from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from collections import Counter


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
        _user = authenticate(username=_username, password=_password)
        if _user is not None:
            return True
        else:
            return False

    # Changes the password of an individual user supplied old and new pass
    def changePassword(self, oldPass, newPass):
        _user = authenticate(username=self.user.username, password=oldPass)
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
            if not friend in self.getFriends():
                self.friends.add(friend)
            return True
        else:
            return False

    def sendFriendRequest(self, friend):
        if isinstance(friend, Profile):
            if not friend in self.getFriends():
                friend.addNotification(
                    message=""+self.user.username+" sent you a friend request.",
                    link="/friends/"+str(self.user.id)+"/request",
                )
            return True
        else:
            return False

    # Removes a friend from the profile
    # user.profile.removeFriend(Profile instance)
    def removeFriend(self, friend):
        if isinstance(friend, Profile):
            if friend in self.getFriends():
                self.friends.remove(friend)
            return True
        else:
            return False

    # Returns the library of the user
    # user.profile.getLibrary()
    def getLibrary(self):
        return self.library.all()

    # Adds a game to a user's library
    # user.profile.addGame(Game instance)
    def addGame(self, game):
        if isinstance(game, Game):
            if not game in self.getLibrary():
                self.library.add(game)
            return True
        else:
            return False

    # Removes a game from the user's library
    # user.profile.removeGame(Game instance)
    def removeGame(self, game):
        if isinstance(game, Game):
            if game in self.getLibrary():
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
            self, message, link
        )

    # Removes a notification from a user
    # user.profile.removeNotification(Notification instance)
    def removeNotification(self, notification):
        if isinstance(notification, Notification):
            if notification in self.getNotifications():
                self.notifications.filter(pk=notification.id).delete()
            return True
        else:
            return False

    # Returns all events a user is hosting
    # user.profile.getEventsHosting()
    def getEventsHosting(self):
        return self.events_hosting.all()

    # Returns all events a user is attending
    # user.profile.getEventsAttending()
    def getEventsAttending(self):
        return self.events_attending.all()

    def getAllEvents(self):
        return self.getEventsHosting() + self.getEventsAttending()



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
        self.get(pk=gameID).delete()
    def getAllGames(self):
        return self.all()

class Game(models.Model):
    gameName = models.CharField(max_length=50, default="")
    playerMin = models.IntegerField()
    playerMax = models.IntegerField()
    genre = models.CharField(max_length=50, default="")
    thumbnail_url = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=10000, default="")
    objects = GameManager()

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
        self.get(pk=eventID).delete()


class Event(models.Model):
    host = models.ForeignKey('profile', on_delete=models.CASCADE, related_name="events_hosting")
    attendees = models.ManyToManyField("profile", related_name="events_attending")
    pendingPlayers = models.ManyToManyField("profile", related_name="events_invited")
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
    def getPendingPlayers(self):
        return self.pendingPlayers.all()

    def getAttendingPlayers(self):
        return self.attendees.all()

    def addPending(self, user):
        if isinstance(user, Profile):
            if not user in self.getPendingPlayers():
                self.pendingPlayers.add(user)
            return True
        else:
            return False

    def removePending(self, user):
        if isinstance(user, Profile):
            if user in self.getPendingPlayers():
                self.pendingPlayers.remove(user)
            return True
        else:
            return False

    def addAttendee(self, user):
        if isinstance(user, Profile):
            if not user in self.attendees.all():
                self.attendees.add(user)
            return True
        else:
            return False

    def removeAttendee(self, user):
        if isinstance(user, Profile):
            if user in self.attendees.all():
                self.attendees.remove(user)
            return True
        else:
            return False

    def sendInvites(self):
        for pp in self.pendingPlayers.all():
            pp.addNotification(
                "You've been invited to join an event hosted by " + self.host.user.username + ".",
                "/events/" + str(self.pk) + "/request",
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

    # Return the event's votese
    # event.getVotes() (returns list of votes)
    def getVotes(self):
        return self.votes.all()


    # Takes all attending players and returns a list representing the union of their libraries
    def getFilteredGames(self):
        groupLibrary = []
        playerNum = len(self.attendees.all())+1
        #adds to list all games that someone owns and matches numberOfPlayers filter (skipping duplicates)
        for profile in self.attendees.all():
            for game in profile.getLibrary():
                if(game not in groupLibrary):
                    gInfo = game.getGame()
                    if(gInfo["minimum_players"]<=playerNum and playerNum<=gInfo["maximum_players"]): #filter for number of players
                        groupLibrary.append(game)
        #do the same for the host
        for game in self.host.getLibrary():
            if(game not in groupLibrary):
                gInfo = game.getGame()
                if(gInfo["minimum_players"]<=playerNum and playerNum<=gInfo["maximum_players"]): #filter for number of players
                    groupLibrary.append(game)
        return groupLibrary #returns a list of game objects


    # Grab all of the votes using self.getVotes(), use the list of votes and their
    # getGame() and getRank() methods to find the top 3, and return the top 3 games
    def getRankedGames(self):
        rankings = {}
        for vote in self.getVotes():
            if vote.getGame() not in rankings:
                rankings[vote.getGame()] = 0
            if(vote.getRank()==1):
                rankings[vote.getGame()] += 3
            elif(vote.getRank()==2):
                rankings[vote.getGame()] += 2
            elif(vote.getRank()==3):
                rankings[vote.getGame()] += 1
        #produces a list of tuples (game, rankScore) of the top 3 games
        gameRanks = Counter(rankings).most_common(3)
        #converts gameranks to a list of top 3 games
        for i in range(len(gameRanks)):
            gameRanks[i] = gameRanks[i][0]
        return gameRanks #returns a list of game objects




class NotificationManager(models.Manager):
    def create_notification(self, profile, message, link):
        notif = self.create(recipient=profile, message=message, link=link)
        notif.save()
        return notif
    def delete_notification(self, msg):
        msg.delete()

class Notification(models.Model):
    recipient = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=100, default="")
    objects = NotificationManager()

class VoteManager(models.Manager):
    def create(self, event, game, rank):
        vote = self.create(event=event, game=game, rank=rank)
        vote.save()
        return vote
    def delete(self, d_vote):
        d_vote.delete()

class Vote(models.Model):
    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        related_name="votes"
    )
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="votes"
    )
    rank = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(3), MinValueValidator(1)]
    )
    objects = VoteManager()

    def getGame(self):
        return self.game

    def getRank(self):
        return self.rank
