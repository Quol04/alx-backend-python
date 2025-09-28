from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrParticipant


# ------------------------
# Conversation ViewSet
# ------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, and creating conversations.
    Only participants can access conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    # Enable filtering & searching
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Limit conversations to only those where the user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects: {"participants": [user_id1, user_id2, ...]}
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"error": "At least one participant is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(participants)
        conversation.participants.add(request.user)  # ensure creator is included

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ------------------------
# Message ViewSet
# ------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, and creating messages.
    Only participants in conversations can access messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrParticipant]

    # Enable filtering & searching
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__email']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        """
        Return messages only for conversations the user participates in.
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation.
        Expects: {"conversation": conversation_id, "message_body": "text here"}
        """
        conversation_id = request.data.get("conversation")
        message_body = request.data.get("message_body")

        if not conversation_id or not message_body:
            return Response({"error": "conversation and message_body are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."},
                            status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
