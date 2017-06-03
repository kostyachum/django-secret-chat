# Django Secret Chat

Allows to generate chat protected by password and allow admin to left answers

## Application

User Views:
- New chat
- Chat view

To access chat and to post messages user have to provide chat password specified when created.
Wrong password on message post redirects to chat login view. All messages from user marks as 'OWNER'.
Password can be empty.

Admin View:
- Chat list
- Chat Respond view

Chat list is sorted by unread first, by create date after. Once chat opened it marks as read, if new message from user added
it marks as new.
All messages from admin have sender 'RESPONDENT'

## API
User Endpoints:
- New Chat
- Chat details
- Chat new message

To get or post chat massages user have to provide chat password. All messages from user marks as 'OWNER'.
Password can be empty.

Admin Views:
- Chat list
- Chat details
- Chat new message

Chat list is sorted by unread first, by create date after. Once chat opened it marks as read, if new message from user added
it marks as new.
All messages from admin have sender 'RESPONDENT'