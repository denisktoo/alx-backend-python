from rest_framework import viewsets, status, filters, generics
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, RegisterSerializer, UserSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import CustomMessagePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied


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
        messages = Message.objects.filter(conversation=conversation_id)

        if not messages.first() or self.request.user not in messages.first().conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant of this conversation.", code=status.HTTP_403_FORBIDDEN)

        return messages
    
    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to send messages to this conversation.")
        serializer.save(sender=self.request.user)

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
    permission_classes = [IsAuthenticated]
