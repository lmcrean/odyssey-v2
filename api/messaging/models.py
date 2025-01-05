# messaging/models.py

from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='messages/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'
