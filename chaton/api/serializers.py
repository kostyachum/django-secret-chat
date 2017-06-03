import hashlib

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


class AddChatSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, source='password_hash', write_only=True)
    hash = serializers.CharField(read_only=True)

    class Meta:
        model = Chat
        fields = ['title', 'password', 'hash']

    def save(self, **kwargs):
        password_hash = hashlib.md5(self.validated_data.get('password_hash', '').encode('utf-8')).hexdigest()
        self.validated_data['password_hash'] = password_hash
        return super(AddChatSerializer, self).save(**kwargs)


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
