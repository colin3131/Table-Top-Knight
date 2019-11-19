from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
import User as UserClass
from database.models import Profile, Game, Event, Notification, Vote
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, VoteForm, EventForm
from database.models import Vote, Event, Game

# Profile Model
class ProfileTest(TestCase):
	def setUp(self):
		User.objects.create_user(username="colin", email="colin@gmail.com", password="testpass123")
		User.objects.create_user(username="connor", email="connor@gmail.com", password="testpass123")
		User.objects.create_user(username="jackson", email="jackson@gmail.com", password="testpass123")
		GameManager.objects.create_game(gameName="pokemonGO", playerMin="1", playerMax="10", genre="RPG", thumbnail_url="pkmn", description="Fun for all ages!")

	def verifyLogin(self): 	
		# Returns True or False
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		self.assertTrue(colin.profile.verifyLogin("colin", "testpass123"))

	def changePassword(self):
		# Returns True or False (based on success)
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		colin.profile.set_password(password="newpass123")
		self.assertTrue(colin.profile.changePassword("testpass123", "newpass123"))

	def addFriend(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		self.assertTrue(connor.profile.addFriend(colin))

	def removeFriend(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		self.assertTrue(connor.profile.removeFriend(colin))
	
	def getLibrary():
		# Returns a list of owned games
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		jackson.addGame(pokemonGO)
		assertTrue(jackson.getLibrary())

	def addGame(self):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		self.assertTrue(jackson.addGame(pokemonGO))

	def removeGame(self):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		self.assertTrue(jackson.removeGame(pokemonGO))

	def getNotifications():
		# Returns a list of all notifications
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		connor.addNotification("You've been added to a game!")
		assertTrue(connor.getNotifications())

	def addNotification(self):
		# Creates a notification for a user
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		self.assertTrue(connor.addNotification("You've been added to a game", "https://google.com"))

	def removeNotification(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		self.assertTrue(connor.removeNotification("You've been added to a game"))

	def getEventsHosting():
		# Returns a list of events a user is hosting
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.getEventsHosting())

	def getEventsAttending():
		# Returns a list of events a user is attending
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.getEventsAttending())

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

		GameManager.objects.create_game(gameName="pokemonGO", playerMin="1", playerMax="10",
		                                genre="RPG", thumbnail_url="pkmn", description="Fun for all ages!")

	def addPending(self):
		# Adds a player to pendingPlayers, returns true/false
		self.assertTrue(event.addPending(connor.profile))

	def removePending(self):
		# Removes a player from pendingPlayers, returns true/false
		self.assertTrue(event.removePending(connor.profile))

	def addAttendee(self):
		# Adds a user to the attendees, returns true/false
		self.assertTrue(event.addAttendee(jackson.profile))

	def removeAttendee(self):
		# Removes a user from the attendees, returns true/false
		self.assertTrue(event.removeAttendee(jackson.profile))

	def sendInvites():
		# Invites all of the players that are currently pending
		event.addPending(connor.profile)
		event.sendInvites()
		self.assertIn()

	def canVote():
		# Returns true if the event is currently in the voting phase
		self.assertTrue(event.canVote())

	def canInvite():
		# Returns true if the event is currently in the invite phase
		self.assertTrue(event.canInvite())

	def canPlay():
		# Returns true if the event is currently in the pre-game phase
		self.assertTrue(event.canPlay())

	def startVoting():
		# Sets the event's state to the Voting phase, returns nothing
		self.assertTrue()

	def endVoting():
		# Sets the event's state to the pre-game phase, returns nothing
		
	def	getFilteredGames():
		# Returns a list of games that users own, filtered by the amount of players

	def getRankedGames():
		# Returns a list of games that have been chosen based on the voting phase

# Game Model
class GameManagerTest(TestCase):
	# Adds a game into the game database
	def create_game():
		game = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thumbnail_url="pkmn", description="It's a game")
		assertTrue(game.gameName == "PokemonGo")
		assertTrue(game.gameMin == 1)
		assertTrue(game.gameMax == 10)
		assertTrue(game.genre == "RPG")
		assertTrue(game.thumbnail_url == "pkmn")
		assertTrue(game.description == "It's a game")
	def delete_game():
		# Removes a game from the game database
		game = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thumbnail_url="pkmn", description="It's a game")
		gameID = game.ID
		Game.objects.delete_game(gameID)
		assertRaises(DoesNotExist, Game.objects.get(pk=gameID))
