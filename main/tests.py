from django.test import TestCase
from django.contrib.auth.models import User
from main.models import BaseEvent


class SubsciptionTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='Sam',password='qwertyuio')
		self.event = BaseEvent.objects.create()


	def test_default_number_of_subscribers(self):
		number_of_subscribers = self.event.num_of_participants
		
		self.assertEqual(number_of_subscribers, 0)


	def test_number_of_subscribers_after_subscribing(self):
		number_of_subscribers_before = self.event.num_of_participants
		self.event.subscribe(self.user)
		number_of_subscribers_after = self.event.num_of_participants

		self.assertEqual(number_of_subscribers_before, number_of_subscribers_after - 1)


	def test_number_of_subscribers_after_unsubscribing(self):
		self.event.subscribe(self.user)
		number_of_subscribers_before = self.event.num_of_participants

		self.event.unsubscribe(self.user)
		number_of_subscribers_after = self.event.num_of_participants

		self.assertEqual(number_of_subscribers_before, number_of_subscribers_after + 1)


	def test_subscription_status(self):
		status = self.event.is_user_subscribed(self.user)
		self.assertEqual(status, False)

		self.event.subscribe(self.user)
		status = self.event.is_user_subscribed(self.user)
		self.assertEqual(status, True)

		self.event.unsubscribe(self.user)
		status = self.event.is_user_subscribed(self.user)
		self.assertEqual(status, False)


