from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
#import User as UserClass
from database.models import Profile, Game, Event, Notification, Vote
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
#from .forms import SignUpForm, VoteForm, EventForm
from database.models import Vote, Event, Game
import datetime

# Profile Model
class ProfileTest(TestCase):
	def setUp(self):
		User.objects.create_user(username="colin", email="colin@gmail.com", password="testpass123")
		User.objects.create_user(username="connor", email="connor@gmail.com", password="testpass123")
		User.objects.create_user(username="jackson", email="jackson@gmail.com", password="testpass123")
		Game.objects.create_game(gameName="pokemonGO", playerMin="1", playerMax="10", genre="RPG", thmb="pkmn", desc="Fun for all ages!")

	def verifyLogin(self): 	
		# Returns True or False
		colin = User.objects.get(username="colin")
		self.assertTrue(colin.profile.verifyLogin("colin", "testpass123"))

	def changePassword(self):
		# Returns True or False (based on success)
		colin = User.objects.get(username="colin")
		colin.profile.set_password(password="newpass123")
		self.assertTrue(colin.profile.changePassword("testpass123", "newpass123"))

	def addFriend(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor")
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		self.assertTrue(connor.profile.addFriend(colin))

	def removeFriend(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor")
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		self.assertTrue(connor.profile.removeFriend(colin))
	
	def getLibrary(self):
		# Returns a list of owned games
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson")
		jackson.addGame(pokemonGO)
		self.assertEqual(pokemonGO, jackson.getLibrary().get(pk=pokemonGO.ID))

	def addGame(self):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson")
		self.assertTrue(jackson.addGame(pokemonGO))

	def removeGame(self):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson")
		self.assertTrue(jackson.removeGame(pokemonGO))

	def getNotifications(self):
		# Returns a list of all notifications
		connor = User.objects.get(username="connor")
		connor.addNotification("You've been added to a game!")
		self.assertTrue(connor.getNotifications())

	def addNotification(self):
		# Creates a notification for a user
		connor = User.objects.get(username="connor")
		self.assertTrue(connor.addNotification("You've been added to a game", "https://google.com"))

	def removeNotification(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor")
		self.assertTrue(connor.removeNotification("You've been added to a game"))

	def getEventsHosting(self):
		# Returns a list of events a user is hosting
		jackson = User.objects.get(username="jackson")
		self.assertTrue(jackson.getEventsHosting())

	def getEventsAttending(self):
		# Returns a list of events a user is attending
		jackson = User.objects.get(username="jackson")
		self.assertTrue(jackson.getEventsAttending())

# Event Model
class EventTest(TestCase):
	def setUp(self):
		User.objects.create_user(
			username="colin", email="colin@gmail.com", password="testpass123")
		User.objects.create_user(
			username="connor", email="connor@gmail.com", password="testpass123")
		User.objects.create_user(
			username="jackson", email="jackson@gmail.com", password="testpass123")

		event = Event.objects.create_event(host=colin.profile, eventDatetime=datetime(
			year=2019, month=10, day=15, hour=15), location="Posvar")

		Game.objects.create_game(gameName="pokemonGO", playerMin="1", playerMax="10", genre="RPG", thmb="pkmn", desc="Fun for all ages!")

	def addPending(self):
		# Adds a player to pendingPlayers, returns true/false
		colin = User.objects.get(username="colin")
		connor = User.objects.get(username="connor")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.addPending(connor.profile))

	def removePending(self):
		# Removes a player from pendingPlayers, returns true/false
		colin = User.objects.get(username="colin")
		connor = User.objects.get(username="connor")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.removePending(connor.profile))

	def addAttendee(self):
		# Adds a user to the attendees, returns true/false
		colin = User.objects.get(username="colin")
		jackson = User.objects.get(username="jackson")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.addAttendee(jackson.profile))

	def removeAttendee(self):
		# Removes a user from the attendees, returns true/false
		colin = User.objects.get(username="colin")
		jackson = User.objects.get(username="jackson")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.removeAttendee(jackson.profile))

	def sendInvites(self):
		# Invites all of the players that are currently pending
		colin = User.objects.get(username="colin")
		connor = User.objects.get(username="connor")
		event = Event.objects.get(host=colin.profile)
		event.addPending(connor.profile)
		event.sendInvites()
		self.assertIn(connor.profile.Notification, connor.getNotifications())

	def canVote(self):
		# Returns true if the event is currently in the voting phase
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.canVote())

	def canInvite(self):
		# Returns true if the event is currently in the invite phase
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.canInvite())

	def canPlay(self):
		# Returns true if the event is currently in the pre-game phase
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.canPlay())

	def startVoting(self):
		# Sets the event's state to the Voting phase, returns nothing
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.startvoting()
		self.assertEqual(event.event_state, event.VOTING)
		
	def endVoting(self):
		# Sets the event's state to the pre-game phase, returns nothing
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.endVoting()		
		self.assertEqual(event.event_state, event.AFTER_VOTING)

	def	getFilteredGames(self):
		# Returns a list of games that users own, filtered by the amount of players
		game1 = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thmb="pkmn", desc="It's a game")
		game2 = Game.objects.create_game(gameName="The Legend of Zelda", playerMin=1, playerMax=1, genre="FirstPerson", thmb="zelda", desc="It's a game")
		game3 = Game.objects.create_game(gameName="Call of Duty", playerMin=1, playerMax=8, genre="FPS", thmb="cod", desc="It's a game")
		gameLibrary = [game1, game2, game3]
		correctOrder = [game2, game3, game1]
		self.assertTrue(gameLibrary[correctOrder])
		
	def getRankedGames(self):
		# Returns a list of games that have been chosen based on the voting phase
# Game Model
class GameManagerTest(TestCase):
	# Adds a game into the game database
	def create_game(self):
		game = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thmb="pkmn", desc="It's a game")
		self.assertTrue(game.gameName == "PokemonGo")
		self.assertTrue(game.gameMin == 1)
		self.assertTrue(game.gameMax == 10)
		self.assertTrue(game.genre == "RPG")
		self.assertTrue(game.thumbnail_url == "pkmn")
		self.assertTrue(game.description == "It's a game")
	def delete_game(self):
		# Removes a game from the game database
		game = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thmb="pkmn", desc="It's a game")
		gameID = game.ID
		Game.objects.delete_game(gameID)
		self.assertRaises(DoesNotExist, Game.objects.get(pk=gameID))
