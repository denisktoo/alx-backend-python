from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'user_id', 'username', 'email', 'phone_number', 'role', 'created_at']


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['url', 'conversation_id', 'participants', 'created_at']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['url', 'message_id', 'conversation', 'sender', 'message_body', 'sent_at']