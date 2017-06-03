from django.conf import settings

CHAT_OWNER = 'o'
CHAT_RESPONDENT = 'r'

MESSAGE_SENDER_CHOICES = (
    (CHAT_OWNER, getattr(settings, 'SECRET_CHAT_OWNER_NAME', 'Owner')),
    (CHAT_RESPONDENT, getattr(settings, 'SECRET_CHAT_RESPONDENT_NAME', 'Respondent')),
)
