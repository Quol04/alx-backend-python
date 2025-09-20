from rest_framework import serializers
from .models import User, Conversation, Message


# ------------------------
# User Serializer
# ------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Exclude password field for security reasons
        exclude = ['password', 'groups', 'user_permissions']


# ------------------------
# Message Serializer
# ------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'conversation',
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['message_id', 'sent_at']


# ------------------------
# Conversation Serializer
# ------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']
