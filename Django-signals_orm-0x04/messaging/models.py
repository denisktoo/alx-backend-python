from django.db import models
from django.db.models import Prefetch
from django.contrib.auth.models import AbstractUser
import uuid
from .managers import UnreadMessagesManager

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
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_by = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.message_id} by {self.sender.email}"
    
    # Managers
    objects = models.Manager()
    unread = UnreadMessagesManager()

    def mark_as_read(self):
        self.read = True
        self.save(update_fields=['read'])
    
    def get_all_replies(self):
        replies = []

        def fetch_replies(msg):
            children = Message.objects.filter(parent_message=msg).select_related('sender', 'receiver')
            for child in children:
                replies.append(child)
                fetch_replies(child)

        fetch_replies(self)
        return replies

Message.objects.select_related('sender', 'receiver').prefetch_related(
    Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
)

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_notifications')
    notification = models.CharField(max_length=128)

    def __str__(self):
        return f"Notification for {self.receiver.first_name}: {self.notification}"

class MessageHistory(models.Model):
    messageHistory_id = models.AutoField(primary_key=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_body = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for: {self.message.message_id} at {self.edited_at}"
