
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^chats/new/$', views.AddChatView.as_view(), name='api-chat-new'),
    url(r'^chats/$', views.ChatListView.as_view(), name='api-chat-list'),
    url(r'^chats/(?P<hash>[-\w]+)/$', views.ChatMessageList.as_view(), name='api-chat-detail'),
    url(r'^chats/respond/(?P<hash>[-\w]+)/$', views.ChatRespondView.as_view(), name='api-chat-respond'),

]
