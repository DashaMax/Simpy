from django.urls import path

from msg.views import ChatMessagesView, ChatsView, GetChatView


urlpatterns = [
    path('', ChatsView.as_view(), name='chats'),
    path('get-chat/<slug:user_slug>/', GetChatView.as_view(), name='get-chat'),
    path('messages/<int:chat_pk>/', ChatMessagesView.as_view(), name='chat-messages'),
]