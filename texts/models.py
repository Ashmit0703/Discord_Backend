from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

class TextMessage(models.Model):
    """
    Model to represent text messages in a common channel
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

    class Meta:
        ordering = ['-created_at']

class MessageDeletionLog(models.Model):
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_content = models.TextField()
    deleted_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Deleted by {self.moderator.username} at {self.deleted_at}"