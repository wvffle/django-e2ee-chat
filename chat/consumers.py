import asyncio
import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.models import Profile, Message, Room, RoomInvite
from chat.serializers import MessageSerializer, RoomInviteSerializer, RoomSerializer
from django_chat.settings import DEBUG


class ChatConsumer(AsyncJsonWebsocketConsumer):
    user = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)

        print(data)
        msg_type = data['type']
        if msg_type == 'login':
            # TODO [#33]: Check if user is authenticated
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

        if msg_type == 'invite.a':
            room = await self.accept_invite(data['invite'])

            await self.channel_layer.group_send(
                f'room-{room.name}',
                {
                    'type': 'send.event',
                    'data': {
                        'type': 'room.j',
                        'room': room.name,
                        'name': self.user.name,
                        'publicKey': self.user.public_key,
                    }
                 },
            )

            await self.subscribe_room({'data': {'name': room.name}})
            return await self.fetch_invites(None)

        if msg_type == 'invite.r':
            await self.remove_invite(data['invite'])
            return await self.fetch_invites(None)

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
        }))

    async def fetch_invites(self, _):
        await self.send(text_data=json.dumps({
            'type': 'invites',
            'invites': await self.get_invites()
        }))

    async def logout(self, _):
        await self.send(text_data=json.dumps({
            'type': 'logout',
        }))

    @database_sync_to_async
    def accept_invite(self, id):
        invite = RoomInvite.objects.filter(id=id).first()
        room = invite.room
        room.participants.add(self.user)
        invite.delete()
        return room

    @database_sync_to_async
    def remove_invite(self, id):
        RoomInvite.objects.filter(id=id).delete()

    @database_sync_to_async
    def set_user(self, name):
        sess_name = self.scope['session']['name']
        if sess_name != name:
            async_to_sync(self.channel_layer.group_send)(
                f'user-{sess_name}',
                {'type': 'logout'},
            )

        self.user = Profile.objects.get(name=name)
        self.scope['session']['name'] = name
        self.scope['session']['profile_id'] = self.user.id

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
        data = RoomInviteSerializer(RoomInvite.objects.filter(invitee=self.user), many=True).data
        rooms = RoomSerializer(Room.objects.filter(name__in=[invite['room'] for invite in data]), many=True).data
        rooms = {room['name']: room for room in rooms}

        invites = []
        for i, invite in enumerate(data):
            invites.append({**invite, 'room': rooms[invite['room']]})

        return invites

    @database_sync_to_async
    def get_room_messages(self, room_name, last_id):
        qs = Message.objects.filter(room__name=room_name)
        if last_id is not None:
            qs = qs.filter(id__lt=last_id)

        return MessageSerializer(qs.order_by('-id').all()[:50], many=True).data
