from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import json

from .models import ChatGroup, GroupMessage

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        print("WebSocket connecting...")
        self.user = self.scope['user']
        self.chatroom = get_object_or_404(ChatGroup, group_name='private_chat') 
        print("WebSocket connected!")
        self.accept()

    def receive(self, text_data):
        print("Received from client:", text_data)
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user.profile,
            group=self.chatroom,
        )

        context = {
            'message': message,
            'user': self.user,
        }

        html = render_to_string("chat_rt/chat_message.html", context=context)

        try:
            self.send(text_data=json.dumps({
                "content": html,
                "target": "#chat-messages",
                "swap": "beforeend"
            }))
            print("WebSocket send successful")
        except Exception as e:
            print("WebSocket send failed:", e)

