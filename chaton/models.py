import base64

from Crypto.Cipher import XOR
from django.contrib.auth.models import User
from django.db import models

from chaton.config import CHAT_RESPONDENT, MESSAGE_SENDER_CHOICES

from django.utils.crypto import get_random_string


class Chat(models.Model):
    password_hash = models.CharField(max_length=1024, null=True, editable=False)
    hash = models.CharField(max_length=64, db_index=True)
    title = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = get_random_string(32)
        return super(Chat, self).save(*args, **kwargs)

    def __str__(self):
        return 'Chat {}'.format(self.hash)


class Message(models.Model):
    chat = models.ForeignKey(Chat, db_index=True)
    sender = models.CharField(max_length=1, choices=MESSAGE_SENDER_CHOICES, default=CHAT_RESPONDENT)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message {} Chat {}'.format(self.pk, self.chat.hash)


class UserChatList(models.Model):
    chat_list = models.TextField()
    user = models.ForeignKey(User, unique=True)

    @staticmethod
    def encrypt(key, plaintext):
        cipher = XOR.new(key)
        return base64.b64encode(cipher.encrypt(plaintext))

    @staticmethod
    def decrypt(key, ciphertext):
        cipher = XOR.new(key)
        return cipher.decrypt(base64.b64decode(ciphertext))
