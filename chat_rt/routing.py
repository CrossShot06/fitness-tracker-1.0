from django.urls import re_path
from .consumers import ChatroomConsumer

websocket_urlpatterns = [
    re_path(r'^ws/chatroom/(?P<chatroom_name>[^/]+)/?$', ChatroomConsumer.as_asgi()),
]