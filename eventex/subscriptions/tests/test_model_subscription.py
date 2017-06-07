from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Herbert Fortes',
            cpf='12345678901',
            email='terberh@gmail.com',
            phone='21-999216226'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """ Subscription must have an auto create_at attr"""
        self.assertIsInstance(self.obj.created_at, datetime)
