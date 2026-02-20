import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.me = self.scope['user']
        self.other_username = self.scope['url_route']['kwargs']['username']
        self.other_user = await self.get_user(self.other_username)
        
        ids = sorted([self.me.id, self.other_user.id])
        self.room_group_name = f'chat_{ids[0]}_{ids[1]}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.mark_messages_as_read()
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'read_receipt_handler', 'reader': self.me.username}
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'message':
            message_text = data.get('message')
            msg_obj = await self.save_message(message_text)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'message_handler',
                    'message': message_text,
                    'sender': self.me.username,
                    'timestamp': msg_obj.timestamp.strftime('%H:%M'),
                    'message_id': msg_obj.id
                }
            )
        
        elif action == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'typing_handler', 'username': self.me.username, 'is_typing': data.get('typing')}
            )

    async def message_handler(self, event):
        if event['sender'] != self.me.username:
            await self.channel_layer.group_send(
                self.room_group_name,
                {'type': 'delivery_receipt_handler', 'message_id': event.get('message_id')}
            )
        await self.send(text_data=json.dumps(event))

    async def delivery_receipt_handler(self, event):
        await self.send(text_data=json.dumps({
            'action': 'delivered_confirmed',
            'message_id': event['message_id']
        }))

    async def read_receipt_handler(self, event):
        await self.send(text_data=json.dumps({'action': 'read_confirmed', 'reader': event['reader']}))

    async def typing_handler(self, event):
        await self.send(text_data=json.dumps({'action': 'typing', 'username': event['username'], 'is_typing': event['is_typing']}))

    @database_sync_to_async
    def get_user(self, username): return User.objects.get(username=username)

    @database_sync_to_async
    def save_message(self, content):
        return Message.objects.create(sender=self.me, receiver=self.other_user, content=content)

    @database_sync_to_async
    def mark_messages_as_read(self):
        return Message.objects.filter(sender=self.other_user, receiver=self.me, is_read=False).update(is_read=True)

