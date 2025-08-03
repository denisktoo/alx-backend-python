from rest_framework import viewsets, status, filters, generics
from .models import Conversation, Message, User, Notification, MessageHistory
from .serializers import ConversationSerializer, MessageSerializer, RegisterSerializer, UserSerializer, NotificationSerializer, MessageHistorySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import CustomMessagePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting Messages.
    """
    serializer_class = MessageSerializer
    pagination_class = CustomMessagePagination
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk') or self.request.query_params.get('conversation_id')
        # messages = Message.objects.filter(conversation=conversation_id)
        request = self.request
        messages = Message.objects.filter(conversation=conversation_id, sender=request.user).select_related('sender', 'receiver').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').only(
            'message_id', 'content', 'timestamp', 'sender__user_id', 'receiver__user_id'
        ))
        )

        if not messages.first() or self.request.user not in messages.first().conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation.", code=status.HTTP_403_FORBIDDEN)

        return messages
    
    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to send messages to this conversation.")
        serializer.save(sender=self.request.user)

class UnreadMessageViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.unread.for_user(self.request.user).filter(conversation_id=conversation_id)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving users.
    Only authenticated users can view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class MessageHistoryViewSet(viewsets.ModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer

class DeleteUserViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_user(self, request):
        user = request.user
        user.delete()

class CachedMessageViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    @action(detail=True, methods=['get'], url_path='cached-messages')
    def list_cached_messages(self, request, pk=None):
        messages = Message.objects.filter(conversation_id=pk).select_related('sender', 'receiver')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)