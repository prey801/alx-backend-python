import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# User model
class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False )
    first_name = models.CharField(
        max_length=255, 
        null=False )
    last_name = models.CharField(
        max_length=255, 
        null=False)
    email = models.EmailField(
        unique=True, 
        null=False)
    # Remove password_hash as AbstractUser already provides password field
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, 
        choices=ROLE_CHOICES, 
        null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

# Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    participants = models.ManyToManyField(
        User,
        related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# Message model
class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sent_messages')
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"
