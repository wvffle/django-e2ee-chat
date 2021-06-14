import base64
import collections
import itertools
import json

from Crypto.Util.Padding import pad
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.core.serializers import serialize

from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.http import JsonResponse
from django.template.context_processors import csrf

from django_chat.settings import HCAPTCHA_SECRET
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from chat.utils import base58
from chat.models import Ban, Room, Message
from chat.serializers import *


def index(request):
    return render(request, 'chat/index.html', context={
        # 'error': True,
        # 'statusCode': 500,
        # 'message': 'test message'
    })


class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer

    def create(self, request, pk=None):
        if 'invite' not in request.data or 'public_key' not in request.data or request.data['invite'] == '' or \
                request.data['public_key'] == '' or 'hcaptcha' not in request.data or request.data['hcaptcha'] == '':
            return Response({
                'success': False,
                'message': 'Pola `hcaptcha`, `public_key` oraz `invite` sa wymagane.'
            }, status=400)

        if HCAPTCHA_SECRET != "":
            hcaptcha_request = Request('https://hcaptcha.com/siteverify', urlencode({
                'secret': HCAPTCHA_SECRET,
                'response': request.data['hcaptcha']
            }).encode())

            hcaptcha_data = json.loads(urlopen(hcaptcha_request).read().decode())
            if hcaptcha_data['success'] is False:
                return Response({
                    'success': False,
                    'message': 'Niepoprawna captcha.'
                }, status=400)

        invite_str = request.data['invite']
        query = Invite.objects.filter(invite=invite_str)
        if not query.exists():
            return Response({
                'success': False,
                'message': 'Zaproszenie nie istnieje.'
            }, status=400)

        invite = query.get()
        if Ban.objects.filter(invite=invite).exists():
            return Response({
                'success': False,
                'message': 'Zaproszenie jest zablokowane.'
            }, status=400)

        for profile in Profile.objects.all():
            if profile.public_key == request.data['public_key']:
                return Response({
                    'success': False,
                    'message': 'Taki użytkownik już istnieje.'
                }, status=403)

        name = base58.random(8)
        profile = Profile(
            invite=invite,
            public_key=request.data['public_key'],
            name=name,
        )

        profile.save()

        return Response({
            'name': name,
            'success': True,
        })


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = LoginSerializer

    def get(self, request, pk=None):
        return Response({
            'name': base58.random(8),
        })

    def create(self, request, pk=None):
        if 'name' not in request.data or request.data['name'] == '':
            return Response({
                'message': 'Uzytkownik nie zostal odnaleziony.',
                'success': False
            }, status=401)

        query = Profile.objects.filter(name=request.data['name'])

        if not query.exists():
            return Response({
                'success': False,
                'message': 'Uzytkownik nie istnieje.'
            }, status=400)

        profile = query.get()
        for ban in Ban.objects.all():
            if ban.is_banned(profile):
                return Response({
                    'message': 'Uzytkownik zostal zbanowany',
                    'success': False
                }, status=403)

        public_key = RSA.import_key(f"-----BEGIN PUBLIC KEY-----\n{profile.public_key}\n-----END PUBLIC KEY-----")
        cipher_rsa = PKCS1_OAEP.new(public_key, SHA512)

        session_key = get_random_bytes(32)
        enc_session_key = cipher_rsa.encrypt(session_key)
        profile.session_key = enc_session_key

        auth_key = base58.random(32)
        request.session['auth_key'] = auth_key

        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        ct_bytes = cipher_aes.encrypt(pad(auth_key.encode("utf-8"), AES.block_size))

        request.session['name'] = request.data['name']
        request.session['authenticated'] = False

        return Response({
            'sessionKey': base64.b64encode(enc_session_key),
            'authKey': base64.b64encode(ct_bytes),
            'iv': base64.b64encode(cipher_aes.iv),
            'success': True,
        })


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('name')
    serializer_class = ProfileSerializer


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all().order_by('invite')
    serializer_class = InviteSerializer


class LoginVerifyViewSet(viewsets.GenericViewSet):
    serializer_class = LoginVerifySerializer

    def create(self, request, pk=None):
        if 'authKey' not in request.data or request.data['authKey'] == '':
            return Response({
                'message': 'Nie podano klucza autentykacyjnego.',
                'success': False
            }, status=400)

        if request.data['authKey'] != request.session['auth_key']:
            return Response({
                'message': 'Nie podano klucza autentykacyjnego.',
                'success': False
            }, status=403)

        profile = Profile.objects.filter(name=request.session['name']).first()
        request.session['profile_id'] = profile.id
        request.session['authenticated'] = True
        return Response({
            'success': True
        }, status=200)


class ProfileRoomsViewSet(viewsets.GenericViewSet):
    serializer_class = RoomSerializer

    def create(self, request, pk=None):
        if 'name' not in request.session or not request.session['authenticated']:
            return Response({
                'success': False,
            }, status=401)

        if 'image' not in request.data or 'name' not in request.data:
            return Response({
                'message': 'Nie podano nazwy lub zdjecia.',
                'success': False
            }, status=400)

        # TODO [#23]: Add image as file
        admin = Profile.objects.get(name=request.session['name'])
        room = Room(admin=admin, display_name=request.data['display_name'], image=request.data['image'], name=base58.random(8))
        room.save()
        room.participants.set([admin])

        return Response({
            'success': True,
            'room': {
                'id': room.id,
                'name': room.name
            }
        })


class MessagesViewSet(viewsets.GenericViewSet):
    serializer_class = MessageSerializer

    def create(self, request):
        if 'name' not in request.session or not request.session['authenticated']:
            return Response({
                'success': False,
            }, status=401)

        if 'room' not in request.data or 'date' not in request.data \
                or 'message' not in request.data or 'retention_seconds' not in request.data:

            return Response({
                'message': 'Nie podano wszystkich pol.',
                'success': False
            }, status=400)

        room_id_qs = Room.objects.filter(name=request.data['room'])

        if not room_id_qs.exists():
            return Response({
                'message': 'Wybrany pokoj nie istnieje.',
                'success': False
            }, status=400)

        room = room_id_qs.get()

        if not room.participants.filter(name=request.session['name']).exists():
            return Response({
                'message': 'Nie jestes czlonkiem wybranego pokoju.',
                'success': False
            }, status=403)

        message = Message(
            room_id=room.id,
            author_id=request.session['profile_id'],
            date=request.data['date'],
            message=request.data['message'],
            retention_seconds=request.data['retention_seconds'],
        )
        message.save()

        data = MessageSerializer(message).data
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'room-{room.name}',
            {
                "type": "send.event",
                "data": {
                    "event": data,
                    "type": "room.m",
                },
            }
        )

        return Response({
            'message': data
        })
