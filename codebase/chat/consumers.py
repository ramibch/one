import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.chat_name = self.scope["url_route"]["kwargs"]["name"]

        try:
            self.chat = Chat.objects.get(name=self.chat_name)
        except Chat.DoesNotExist:
            self.close()

        if not self.user.is_staff and self.chat_name != self.user.username:
            self.close()

        async_to_sync(self.channel_layer.group_add)(self.chat_name, self.channel_name)
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json["message"]
        Message.objects.create(body=body, user=self.user, chat=self.chat)
