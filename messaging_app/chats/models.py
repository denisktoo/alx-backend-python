from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, null=True)
    
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']

    def __str__(self):
        return self.email

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField('User', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} by {self.sender.email}"
