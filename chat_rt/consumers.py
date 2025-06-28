from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
import json

from .models import ChatGroup, GroupMessage

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        print("WebSocket connecting...")
        self.user = self.scope['user']
        self.chatroom = get_object_or_404(ChatGroup,  group_name=self.scope['url_route']['kwargs']['chatroom_name']) 
        print("WebSocket connected!")

        self.chatroom_name = f"chat_{self.chatroom.group_name}"


        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,self.channel_name
        )

    def receive(self, text_data):
        print("Received from client:", text_data)
        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user.profile,
            group=self.chatroom,
        )

        event = {
            'type' : 'message_handler',
            'message_id':message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,event
        )

        print("WebSocket send successful")

    def message_handler(self,event):

        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)

        context = {
            'message': message,
            'user': self.user,
        }

        html = render_to_string("chat_rt/chat_message.html", context=context)

        self.send(text_data=json.dumps({
            "content": html,
            "target": "#chat-messages",
            "swap": "beforeend"
        }))

       

