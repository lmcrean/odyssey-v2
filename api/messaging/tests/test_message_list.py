# File: drf_api/messaging/tests/test_message_list.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message

User = get_user_model()

class MessageListTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.user3 = User.objects.create_user(username='user3', password='pass')
        
        # Create test messages
        Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Message 1 from user1 to user2'
        )
        Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            content='Message 2 from user2 to user1'
        )
        Message.objects.create(
            sender=self.user1,
            recipient=self.user3,
            content='Message 3 from user1 to user3'
        )
        
    def test_message_list_for_user(self):
        """Test that a user can see their messages"""
        messages = Message.objects.filter(
            sender=self.user1
        ) | Message.objects.filter(
            recipient=self.user1
        )
        self.assertEqual(messages.count(), 2)
        
    def test_message_privacy(self):
        """Test that a user cannot see messages they're not part of"""
        messages = Message.objects.filter(
            sender=self.user3
        ) | Message.objects.filter(
            recipient=self.user3
        )
        self.assertEqual(messages.count(), 1)