
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^chats/(?P<hash>[-\w]+)/$', views.ChatMessageList.as_view(), name='api-chat-detail'),
    url(r'^chats/respond/(?P<hash>[-\w]+)/$', views.ChatRespondView.as_view(), name='api-chat-respond'),
    url(r'^chats/$', views.ChatListView.as_view(), name='api-chat-list'),
]
