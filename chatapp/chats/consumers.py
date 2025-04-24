import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', 'Anonymous')
        message_id = text_data_json.get('message_id', '')  # Unique ID for acknowledgment

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'message_id': message_id,
                'sender_channel_name': self.channel_name  # Add sender's channel name
            }
        )

        # Send acknowledgment to sender
        await self.send(text_data=json.dumps({
            'type': 'ack',
            'message_id': message_id,
            'status': 'delivered'
        }))

    async def chat_message(self, event):
        # Send message to WebSocket clients
        if event.get('sender_channel_name') != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': event['message'],
                'username': event['username'],
                'message_id': event['message_id']
            }))