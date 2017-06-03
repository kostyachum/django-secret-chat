from rest_framework import serializers

from chaton.models import Message, Chat


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message', 'sent', 'sender']


class ChatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['title', 'hash', 'created', 'unread']


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(source='message_set', many=True)

    class Meta:
        model = Chat
        fields = ['title', 'hash', 'created', 'unread', 'messages']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(source='message_set', many=True)

    class Meta:
        model = Chat
        fields = ['title', 'messages']