import hashlib

from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from chaton.api import serializers
from .. import config
from ..models import Chat


class ChatListView(ListAPIView):
    """
    Chat list without password
    """
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = super(ChatListView, self).get_queryset()
        return queryset.order_by('-unread', '-created')


class ChatRespondView(RetrieveAPIView):
    """
    Chat response view,
    GET: chat details
    POST: adds new message as RESPONDENT
    """
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatDetailSerializer
    permission_classes = [IsAdminUser]

    lookup_field = 'hash'
    lookup_url_kwarg = 'hash'
    
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.unread = False
        obj.save()
        return super(ChatRespondView, self).get(request, *args, **kwargs)
    
    def post(self, request, hash):
        """
        Adds new message to the chat
        message -- message text
        password -- chat password
        """
        chat = self.get_object()
        serializer = serializers.MessageSerializer(data=request.data)
        if serializer.is_valid():
            return self._save_message(chat, serializer)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @classmethod
    def _save_message(cls, chat, serializer):
        serializer.validated_data['sender'] = config.CHAT_RESPONDENT
        serializer.validated_data['chat'] = chat
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class AddChatView(CreateAPIView):
    serializer_class = serializers.AddChatSerializer


class ChatMessageList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, hash):
        """
        Chat view with messages

        password -- chat password
        """
        chat = self._get_object(hash)
        self._validate_password(chat, request.query_params)
        serializer = serializers.ChatSerializer(chat)
        return Response(serializer.data)

    def post(self, request, hash):
        """
        Adds new message to the chat
        message -- message text
        password -- chat password
        """
        chat = self._get_object(hash)
        self._validate_password(chat, request.data)
        serializer = serializers.MessageSerializer(data=request.data)
        if serializer.is_valid():
            return self._save_message(chat, serializer)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def _validate_password(self, chat, data):
        if chat.password_hash != self._get_password_hash(data):
            raise ValidationError('Wrong password')

    @classmethod
    def _save_message(cls, chat, serializer):
        serializer.validated_data['sender'] = config.CHAT_OWNER
        serializer.validated_data['chat'] = chat
        serializer.save()
        chat.unread = True
        chat.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @classmethod
    def _get_password_hash(cls, data):
        password = data.get('password', '')
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        return password_hash

    @classmethod
    def _get_object(cls, hash):
        try:
            return Chat.objects.get(hash=hash)
        except Chat.DoesNotExist:
            raise NotFound
