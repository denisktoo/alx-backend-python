from rest_framework import permissions

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view it.
    """

    def has_object_permission(self, request, view, obj):
        # obj here is a Conversation instance
        return request.user in obj.participants.all()