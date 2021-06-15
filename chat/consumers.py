import asyncio
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models import Profile, Message, Room
from chat.serializers import MessageSerializer
from django_chat.settings import DEBUG


class ChatConsumer(AsyncJsonWebsocketConsumer):
    user = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        msg_type = data['type']
        if msg_type == 'login':
            await self.set_user(data['name'])

            rooms, invites = await asyncio.gather(
                self.get_rooms(),
                self.get_invites(),
            )

            return await asyncio.gather(
                self.send(text_data=json.dumps({
                    'type': 'rooms',
                    'rooms': rooms
                })),
                self.send(text_data=json.dumps({
                    'type': 'invites',
                    'invites': invites
                })),
                *[
                    self.channel_layer.group_add(f'room-{room["name"]}', self.channel_name)
                    for room in rooms
                ],
                self.channel_layer.group_add(f'user-{data["name"]}', self.channel_name),
            )

        if msg_type == 'room.f':
            return await self.send(text_data=json.dumps({
                'type': 'room.m.l',
                'room': data['room'],
                'lastEvent': data['lastEvent'],
                'events': await self.get_room_messages(data['room'], data['lastEvent']),
            }))

        # NOTE: In development mode, we echo the packets that are unknown to us
        if DEBUG:
            await self.send(text_data=json.dumps(data))

    async def send_event(self, data):
        await self.send(text_data=json.dumps(data['data']))

    async def subscribe_room(self, room):
        rooms, _ = await asyncio.gather(
            self.get_rooms(),
            self.channel_layer.group_add(f'room-{room["data"]["name"]}', self.channel_name),
        )

        await self.send(text_data=json.dumps({
            'type': 'rooms',
            'rooms': rooms,
            'forceSelect': room['data']['name']
        })),

    @database_sync_to_async
    def set_user(self, name):
        self.user = Profile.objects.get(name=name)

    @database_sync_to_async
    def get_rooms(self):
        return [{
            'name': model.name,
            'display_name': model.display_name,
            'image': model.image.url,
            'last_message': MessageSerializer(Message.objects.filter(room=model.id).last()).data,
            'participants': [
                {'name': x[0], 'public_key': x[1]}
                for x in model.participants.values_list('name', 'public_key')
            ],
            'admin': model.admin.name == self.user.name
        } for model in Room.objects.filter(participants__name=self.user.name).all()]

    @database_sync_to_async
    def get_invites(self):
        pass

    @database_sync_to_async
    def get_room_messages(self, room_name, last_id):
        qs = Message.objects.filter(room__name=room_name)
        if last_id is not None:
            qs = qs.filter(id__lt=last_id)

        return MessageSerializer(qs.order_by('-id').all()[:50], many=True).data
