from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    is_sender = serializers.SerializerMethodField()

    def get_is_sender(self, obj):
        request = self.context.get('request')
        return request.user == obj.sender if request else False

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'content',
            'image', 'timestamp', 'read', 'is_sender'
        ]