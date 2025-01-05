from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from ..models import Message
from ..serializers import MessageSerializer

User = get_user_model()


class MessageDetailSendView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        recipient_id = self.kwargs.get('pk')
        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            raise ValidationError('Recipient not found')
        
        serializer.save(sender=self.request.user, recipient=recipient)