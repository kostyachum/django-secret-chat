# Django Secret Chat

Allows to generate chat protected by password and allow admin to left answers

## Features
- Admin don't need anything to see messages and reply, just be an admin (or whatever role is choosen by product);
- User don't need anything if he want just save chat link, or only his password if he wants to store encypted list of chats;
- No user relations;
- Chat can be shared to other people if needed;
- Chat can be protected by password;


## Application

User Views:
- New chat
- Chat view

To access chat and to post messages user have to provide chat password specified when created.
Wrong password on message post redirects to chat login view. All messages from user marks as 'OWNER'.
Password can be empty.

Each user have list of chats that is encrypted by user's password. At the moment list is shown to user on chat page only.

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


## Prototype restrictions
Encryped user's chat lists are implemented just to show the flow, not user friendly due time resctrictions. Right now will be issues when user uses some other password for chat. Better expirience would ne to have seperated password for user's chat list. Could be decided by product owner.
