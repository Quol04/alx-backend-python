from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessagingSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password")
        self.receiver = User.objects.create_user(username="bob", password="password")

    def test_notification_created_on_new_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello Bob!")
        notification = Notification.objects.filter(user=self.receiver, message=msg).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, msg)
