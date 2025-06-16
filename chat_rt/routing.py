from django.urls import re_path
from .consumers import ChatroomConsumer

websocket_urlpatterns = [
    re_path(r"ws/chatroom/private-chat/?$", ChatroomConsumer.as_asgi()),
]