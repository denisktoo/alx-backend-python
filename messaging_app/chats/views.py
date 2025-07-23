from rest_framework import viewsets, status, filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .auth import JWTAuthentication
from .filters import MessageFilter
from .pagination import CustomMessagePagination
from django_filters.rest_framework import DjangoFilterBackend


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsParticipantOfConversation]

    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name']


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating, and deleting Messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']
    pagination_class = CustomMessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
