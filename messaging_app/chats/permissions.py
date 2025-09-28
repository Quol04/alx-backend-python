"""
Custom permission classes for the messaging app.
These permissions ensure proper access control for conversations and messages.
"""

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Conversation, Message


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    
    This permission class ensures that:
    1. Only authenticated users can access the API
    2. Only participants in a conversation can view, create, update, or delete messages
    3. Only participants can view or modify conversation details
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated before allowing any access.
        """
        # Only authenticated users can access the API
        if not request.user or not request.user.is_authenticated:
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        Works for both Conversation and Message objects.
        """
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Get the conversation object
        if isinstance(obj, Conversation):
            conversation = obj
        elif isinstance(obj, Message):
            conversation = obj.conversation
        else:
            # If it's neither a Conversation nor Message, deny access
            return False
        
        # Check if the user is a participant
        is_participant = conversation.participants.filter(user_id=request.user.user_id).exists()
        
        # SAFE METHODS: GET, HEAD, OPTIONS → only participants can view
        if request.method in permissions.SAFE_METHODS:
            return is_participant
        
        # WRITE METHODS: POST, PUT, PATCH, DELETE → only participants can modify
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return is_participant


class IsOwnerOrParticipant(BasePermission):
    """
    Permission class that allows access to owners or participants.
    Useful for messages where the sender should always have access,
    plus all participants in the conversation.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is either the owner of the object or a participant.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # For Message objects
        if isinstance(obj, Message):
            # Allow if user is the sender of the message
            if obj.sender.user_id == request.user.user_id:
                return True
            # Or if user is a participant in the conversation
            return obj.conversation.participants.filter(user_id=request.user.user_id).exists()
        
        # For Conversation objects
        elif isinstance(obj, Conversation):
            # Allow if user is a participant in the conversation
            return obj.participants.filter(user_id=request.user.user_id).exists()
        
        return False


class IsAuthenticatedAndOwner(BasePermission):
    """
    Permission class that only allows owners of an object to access it.
    Useful for user-specific resources.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if object has an owner field
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # Check if object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object has a sender field (for messages)
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        
        return False


class IsParticipantOrReadOnly(BasePermission):
    """
    Permission class that allows participants full access,
    but others only read access (if they somehow get access).
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Allow full access to participants, read-only to others.
        """
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Get the conversation
        if isinstance(obj, Conversation):
            conversation = obj
        elif isinstance(obj, Message):
            conversation = obj.conversation
        else:
            return False
        
        # Check if user is a participant
        is_participant = conversation.participants.filter(user_id=request.user.user_id).exists()
        
        if is_participant:
            return True
        
        # If not a participant, only allow safe methods (GET, HEAD, OPTIONS)
        return request.method in permissions.SAFE_METHODS