from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow only authenticated users (user.is_authenticated)
    - Allow only participants of a conversation to send (POST), view, update (PUT/PATCH), delete (DELETE) messages
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            if user not in obj.conversation.participants.all():
                return False

            if request.method in ["PUT", "PATCH", "DELETE", "POST"]:
                return True

            if request.method in permissions.SAFE_METHODS:
                return True

        return False
