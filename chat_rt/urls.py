from django.urls import path
from .views import chat_view,get_or_create_chatroom

urlpatterns = [
    path('', chat_view, name='chat-home'),
    path('<username>',get_or_create_chatroom,name="start-chat"),
    path('room/<chatroom_name>',chat_view,name="chatroom"),
] 