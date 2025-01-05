# File: messaging/tests/test_message_serializer.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message
from messaging.serializers import MessageSerializer

User = get_user_model()

class MessageSerializerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        
        self.message_data = {
            'sender': self.user1,
            'recipient': self.user2,
            'content': 'Test message'
        }
        
        self.message = Message.objects.create(**self.message_data)
        
    def test_contains_expected_fields(self):
        """Test that serializer contains expected fields"""
        serializer = MessageSerializer(self.message)
        expected_fields = {
            'id', 'sender', 'recipient', 'content', 'image',
            'timestamp', 'read', 'is_sender'
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)
        
    def test_content_field_content(self):
        """Test that content field contains correct data"""
        serializer = MessageSerializer(self.message)
        self.assertEqual(serializer.data['content'], self.message_data['content'])