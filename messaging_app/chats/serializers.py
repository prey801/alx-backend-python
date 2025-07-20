from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_username', 'message_body', 'sent_at']
        
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'last_message', 'participant_count', 'created_at']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        return MessageSerializer(last_message).data if last_message else None

    def get_participant_count(self, obj):
        return obj.participants.count()
