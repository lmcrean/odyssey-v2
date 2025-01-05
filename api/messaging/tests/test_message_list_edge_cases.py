from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message

User = get_user_model()

class MessageListEdgeCasesTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        
        # Create test messages
        Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Test message 1'
        )
        Message.objects.create(
            sender=self.user2,
            recipient=self.user1,
            content='Test message 2'
        )
