from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True) #, source='messages'

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_count', 'messages', 'created_at']

    def get_participant_count(self, obj):
        return obj.participants.count()

class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def create(self, validated_data):
        """
        Attach the authenticated user as the sender.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['sender'] = request.user
        return super().create(validated_data)
