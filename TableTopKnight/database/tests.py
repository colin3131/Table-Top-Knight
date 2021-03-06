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

	def test_verifyLogin(self):
		# Returns True or False
		colin = User.objects.get(username = "colin")
		self.assertTrue(colin.profile.verifyLogin("colin", "testpass123"))

	def test_changePassword(self):
		# Returns True or False (based on success)
		colin = User.objects.get(username="colin")
		self.assertTrue(colin.profile.changePassword("testpass123", "newpass123"))

	def test_addFriend(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor")
		colin = User.objects.get(username="colin")
		self.assertTrue(connor.profile.addFriend(colin.profile))

	def test_removeFriend(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor")
		colin = User.objects.get(username="colin")
		connor.profile.addFriend(colin.profile) # <-- Added this, tests don't always run in order
		self.assertTrue(connor.profile.removeFriend(colin.profile))

	def test_getLibrary(self):
		# Returns a list of owned games
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson")
		jackson.profile.addGame(pokemonGO)
		self.assertEqual(pokemonGO, jackson.profile.getLibrary().get(pk=pokemonGO.id))

	def test_addGame(self):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson")
		self.assertTrue(jackson.profile.addGame(pokemonGO))

	def test_removeGame(self):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson")
		jackson.profile.addGame(pokemonGO)
		self.assertTrue(jackson.profile.removeGame(pokemonGO))

	def test_getNotifications(self):
		# Returns a list of all notifications
		connor = User.objects.get(username="connor")
		connor.profile.addNotification("You've been added to a game!", "gamelink") # Added link field
		self.assertEqual(connor.profile.getNotifications().first().message, "You've been added to a game!") # Grabbed the first notification.message

	def test_addNotification(self):
		# Creates a notification for a user
		connor = User.objects.get(username="connor")
		connor.profile.addNotification("You've been added to a game", "https://google.com")
		self.assertTrue(connor.profile.getNotifications().first().message == "You've been added to a game")

	def test_removeNotification(self):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor")
		connor.profile.addNotification("You've been added to a game!", "gamelink")
		self.assertTrue(connor.profile.removeNotification(Notification.objects.get(message="You've been added to a game!"))) # Gotta remove a notification object

	def test_getEventsHosting(self):
		# Returns a list of events a user is hosting
		jackson = User.objects.get(username="jackson")
		event = Event.objects.create_event(host=jackson.profile, eventDateTime=datetime.date(year=2019, month=10, day=15), location="Posvar")
		self.assertEqual(jackson.profile.getEventsHosting().first(), event) # Can't assert true, have to assert for equality

	def test_getEventsAttending(self):
		# Returns a list of events a user is attending
		jackson = User.objects.get(username="jackson")
		connor = User.objects.get(username="connor")
		event = Event.objects.create_event(host=connor.profile, eventDateTime=datetime.date(year=2019, month=10, day=15), location="Posvar")
		event.addAttendee(jackson.profile)
		self.assertEqual(jackson.profile.getEventsAttending().first(), event)

# Event Model
class EventTest(TestCase):
	def setUp(self):
		colin = User.objects.create_user(username="colin", email="colin@gmail.com", password="testpass123")
		User.objects.create_user(username="connor", email="connor@gmail.com", password="testpass123")
		User.objects.create_user(username="jackson", email="jackson@gmail.com", password="testpass123")
		Event.objects.create_event(host=colin.profile, eventDateTime=datetime.date(year=2019, month=10, day=15), location="Posvar")
		Game.objects.create_game(gameName="pokemonGO", playerMin="1", playerMax="10", genre="RPG", thmb="pkmn", desc="Fun for all ages!")

	def test_addPending(self):
		# Adds a player to pendingPlayers, returns true/false
		colin = User.objects.get(username="colin")
		connor = User.objects.get(username="connor")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.addPending(connor.profile))

	def test_removePending(self):
		# Removes a player from pendingPlayers, returns true/false
		colin = User.objects.get(username="colin")
		connor = User.objects.get(username="connor")
		event = Event.objects.get(host=colin.profile)
		event.addPending(connor.profile)
		self.assertTrue(event.removePending(connor.profile))

	def test_addAttendee(self):
		# Adds a user to the attendees, returns true/false
		colin = User.objects.get(username="colin")
		jackson = User.objects.get(username="jackson")
		event = Event.objects.get(host=colin.profile)
		self.assertTrue(event.addAttendee(jackson.profile))

	def test_removeAttendee(self):
		# Removes a user from the attendees, returns true/false
		colin = User.objects.get(username="colin")
		jackson = User.objects.get(username="jackson")
		event = Event.objects.get(host=colin.profile)
		event.addAttendee(jackson.profile)
		self.assertTrue(event.removeAttendee(jackson.profile))

	def test_sendInvites(self):
		# Invites all of the players that are currently pending
		colin = User.objects.get(username="colin")
		connor = User.objects.get(username="connor")
		event = Event.objects.get(host=colin.profile)
		event.addPending(connor.profile)
		event.sendInvites()
		self.assertEqual("You've been invited to join an event hosted by colin.", connor.profile.getNotifications().first().message)

	def test_canVote(self):
		# Returns true if the event is currently in the voting phase
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.event_state = 'VO'
		event.save()
		self.assertTrue(event.canVote())

	def test_canInvite(self):
		# Returns true if the event is currently in the invite phase
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.event_state = 'PV'
		event.save()
		self.assertTrue(event.canInvite())

	def test_canPlay(self):
		# Returns true if the event is currently in the pre-game phase
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.event_state = 'AV'
		event.save()
		self.assertTrue(event.canPlay())

	def test_startVoting(self):
		# Sets the event's state to the Voting phase, returns nothing
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.startVoting()
		self.assertEqual(event.event_state, 'VO')

	def test_endVoting(self):
		# Sets the event's state to the pre-game phase, returns nothing
		colin = User.objects.get(username="colin")
		event = Event.objects.get(host=colin.profile)
		event.endVoting()
		self.assertEqual(event.event_state, 'AV')

	#def test_getFilteredGames(self):
		# Returns a list of games that users own, filtered by the amount of players
	#	game1 = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thmb="pkmn", desc="It's a game")
	#	game2 = Game.objects.create_game(gameName="The Legend of Zelda", playerMin=1, playerMax=1, genre="FirstPerson", thmb="zelda", desc="It's a game")
	#	game3 = Game.objects.create_game(gameName="Call of Duty", playerMin=1, playerMax=8, genre="FPS", thmb="cod", desc="It's a game")
	#	gameLibrary = [game1, game2, game3]
	#	correctOrder = [game2, game3, game1]
	#	self.assertTrue(test_getFilteredGames(gameLibrary[correctOrder]))


# Game Model
class GameManagerTest(TestCase):
	# Adds a game into the game database
	def test_create_game(self):
		game = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thmb="pkmn", desc="It's a game")
		self.assertTrue(game.gameName == "PokemonGo")
		self.assertTrue(game.playerMin == 1)
		self.assertTrue(game.playerMax == 10)
		self.assertTrue(game.genre == "RPG")
		self.assertTrue(game.thumbnail_url == "pkmn")
		self.assertTrue(game.description == "It's a game")

	def test_delete_game(self):
		# Removes a game from the game database
		game = Game.objects.create_game(gameName="PokemonGo", playerMin=1, playerMax=10, genre="RPG", thmb="pkmn", desc="It's a game")
		gameID = game.id
		Game.objects.delete_game(gameID)
		self.assertRaises(Game.DoesNotExist, Game.objects.get, pk=game.id)
