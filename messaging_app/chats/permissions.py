from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated users who are participants in a conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.participants.all()
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in obj.participants.all()
        return request.user in obj.participants.all()
