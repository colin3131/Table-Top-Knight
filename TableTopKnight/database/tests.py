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
