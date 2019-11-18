from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
import User as UserClass
from database.models import Profile, Game, Event, Notification, Vote
import unittest

# Create your tests here.
class ProfileTest(TestCase):
	def setUp(self):
		User.objects.create_user(username="colin", email="colin@gmail.com", password="testpass123")
		User.objects.create_user(username="connor", email="connor@gmail.com", password="testpass123")
		User.objects.create_user(username="jackson", email="jackson@gmail.com", password="testpass123")
		GameManager.objects.create_game(gameName="pokemonGO", playerMin="1", playerMax="10", genre="RPG", thumbnail_url="pkmn", description="Fun for all ages!")

	def verifyLogin(string:username, string:password): 	
		# Returns True or False
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		assertTrue(colin.profile.verifyLogin("colin", "testpass123"))

	def changePassword(string:oldpass, string:newpass):
		# Returns True or False (based on success)
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		colin.profile.set_password(password="newpass123")
		assertTrue(colin.profile.changePassword("testpass123", "newpass123"))

	def addFriend(Profile:new_friend):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		assertTrue(connor.profile.addFriend(colin))

	def removeFriend(Profile:old_friend):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		colin = User.objects.get(username="colin", email="colin@gmail.com", password="testpass123")
		assertTrue(connor.profile.removeFriend(colin))
	
	def getLibrary():
		# Returns a list of owned games
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.getLibrary())

	def addGame(Game:new_game):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.addGame(pokemonGO))

	def removeGame(Game:old_game):
		# Returns True or False (based on success)
		pokemonGO = Game.objects.get(gameName="pokemonGO")
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.removeGame(pokemonGO))

	def getNotifications():
		# Returns a list of all notifications
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		assertTrue(connor.getNotifications())

	def addNotification(string:message, string:link):
		# Creates a notification for a user
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		assertTrue(connor.addNotification("You've been added to a game", "https://google.com"))

	def removeNotification(notification:old_note):
		# Returns True or False (based on success)
		connor = User.objects.get(username="connor", email="connor@gmail.com", password="testpass123")
		assertTrue(connor.removeNotification("You've been added to a game"))

	def getEventsHosting():
		# Returns a list of events a user is hosting
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.getEventsHosting())

	def getEventsAttending():
		# Returns a list of events a user is attending
		jackson = User.objects.get(username="jackson", email="jackson@gmail.com", password="testpass123")
		assertTrue(jackson.getEventsAttending())
