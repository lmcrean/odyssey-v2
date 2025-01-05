from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class MessageListMostRecentTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        
        # Create test messages with different timestamps
        Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Old message',
            timestamp=timezone.now() - timedelta(days=1)
        )
        Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            content='Recent message',
            timestamp=timezone.now()
        )
        
    def test_messages_ordered_by_timestamp(self):
        """Test that messages are ordered by timestamp descending"""
        messages = Message.objects.all().order_by('-timestamp')
        self.assertEqual(messages.count(), 2)
        self.assertEqual(messages[0].content, 'Recent message')
        self.assertEqual(messages[1].content, 'Old message')