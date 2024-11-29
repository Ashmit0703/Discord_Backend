from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model to support different roles
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User')
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    
    def __str__(self):
        return self.username