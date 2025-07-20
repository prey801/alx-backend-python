from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('api/', views.ChatListCreateView.as_view(), name='chat-list-create'),
    path('api/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path('api/messages/', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('api/messages/<int:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
]