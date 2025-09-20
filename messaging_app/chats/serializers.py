from rest_framework import serializers
from .models import User, Conversation, Message


# ------------------------
# User Serializer
# ------------------------
class UserSerializer(serializers.ModelSerializer):
    # Explicit password field (write-only)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']

    def validate_password(self, value):
        """
        Custom validation for password length & strength.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        """
        Override create to properly hash the password.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # hashes the password
        user.save()
        return user


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

    # Extra field showing number of messages
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'message_count',
            'created_at',
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """
        Count number of messages in this conversation.
        """
        return obj.messages.count()
