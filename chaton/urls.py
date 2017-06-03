
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ChatCreateView.as_view(), name='new'),
    url(r'^list/$', views.ChatListView.as_view(), name='list'),
    url(r'^respond/(?P<hash>[-\w]+)/', views.ChatRespondView.as_view(), name='chat-respond'),

    url(r'^(?P<hash>[-\w]+)/$', views.ChatDetailView.as_view(), name='chat'),
]

