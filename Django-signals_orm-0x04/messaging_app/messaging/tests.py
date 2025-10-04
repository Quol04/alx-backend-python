from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory


class MessageEditHistoryTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="alice", password="password")
        self.receiver = User.objects.create_user(username="bob", password="password")
        self.message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content="Original Message"
        )

    def test_message_edit_creates_history(self):
        # Edit message
        self.message.content = "Updated Message"
        self.message.save()

        # Check history
        history = MessageHistory.objects.filter(message=self.message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original Message")
        self.assertTrue(self.message.edited)
