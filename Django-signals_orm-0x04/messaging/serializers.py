from rest_framework import serializers
from .models import User, Conversation, Message, Notification, MessageHistory
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='participants'
    )
    messages_ids = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, source='messages'
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'participant_count', 'messages_ids', 'created_at']

    def get_participant_count(self, obj):
        return obj.participants.count()
    
    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'parent_message', 'replies', 'read']

    def get_replies(self, obj):
        replies = obj.replies.select_related('sender', 'receiver').all()
        return MessageSerializer(replies, many=True, context=self.context).data

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def create(self, validated_data):
        """
        Attach the authenticated user as the sender.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['sender'] = request.user
        else:
            raise serializers.ValidationError("Sender must be authenticated.")
        return super().create(validated_data)
    
class NotificationSerializer(serializers.ModelSerializer):
    receiver = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '--all--'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class MessageHistorySerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)

    class Meta:
        model = MessageHistory
        fields = ['message_id', 'message', 'old_body', 'edited_at']
