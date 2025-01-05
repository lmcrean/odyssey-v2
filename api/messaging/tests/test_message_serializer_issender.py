# messaging/tests/test_message_serializer_issender.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message
from messaging.serializers import MessageSerializer

User = get_user_model()

class MessageSerializerIsSenderTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        
        self.message = Message.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Test message'
        )
        
    def test_is_sender_field(self):
        """Test that is_sender field is True for sender and False for recipient"""
        serializer = MessageSerializer(self.message, context={'request': type('Request', (), {'user': self.user1})()})
        self.assertTrue(serializer.data['is_sender'])
        
        serializer = MessageSerializer(self.message, context={'request': type('Request', (), {'user': self.user2})()})
        self.assertFalse(serializer.data['is_sender'])