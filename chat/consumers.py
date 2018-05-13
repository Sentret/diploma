import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from main.models import Message
from account.pairing import inverse_cantor_pairing

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        # self.room_group_name = ''.join(sorted(self.room_name))

        self.room_group_name = str (self.scope['user'].id)
        

        inverse_cantor = inverse_cantor_pairing( int(self.room_name) )
        inverse_cantor.remove(self.scope['user'].id)
        recipient_id = inverse_cantor[0]
        self.recipient = User.objects.get(pk=recipient_id)




        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()

            
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        Message.objects.create(addresser=self.scope['user'], recipient=self.recipient, message=message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            str(self.recipient.id),
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))