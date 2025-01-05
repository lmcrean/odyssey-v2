# views/message_list_view.py

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import Message
from ..serializers import MessageSerializer

User = get_user_model()


class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).order_by('-timestamp')

    def perform_create(self, serializer):
        recipient_id = self.request.data.get('recipient')
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            raise ValidationError('Recipient not found')
        
        serializer.save(sender=self.request.user, recipient=recipient)