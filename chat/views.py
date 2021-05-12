import json

from django.core.cache import cache

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django_chat.settings import HCAPTCHA_SECRET
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from chat.utils import base58
from chat.models import Profile, Invite, Ban
from chat.serializers import ProfileSerializer, InviteSerializer, RegisterSerializer, LoginSerializer


def index(request):
    return render(request, 'chat/index.html', context={
        # 'error': True,
        # 'statusCode': 500,
        # 'message': 'test message'
    })


class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer

    def create(self, request, pk=None):
        if 'invite' not in request.data or 'public_key' not in request.data or request.data['invite'] == '' or request.data['public_key'] == ''  or 'hcaptcha' not in request.data or request.data['hcaptcha'] == '':
            return Response({
                'success': False,
                'message': 'Pola `hcaptcha`, `public_key` oraz `invite` sa wymagane.'
            }, status=400)

        if HCAPTCHA_SECRET != "":
            request = Request('https://hcaptcha.com/siteverify', urlencode({
                'secret': HCAPTCHA_SECRET,
                'response': request.data['hcaptcha']
            }).encode())

            hcaptcha_data = json.loads(urlopen(request).read().decode())
            if hcaptcha_data['success'] is False:
                return Response({
                    'success': False,
                    'message': 'Niepoprawna captcha.'
                }, status=400)

        query = Invite.objects.filter(invite=request.data['invite'])
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
        id = {
            'id': base58.random(8),
        }
        return Response(id)

    def create(self, request, pk=None):
        # TODO [$609b97d420133e06d703813e]:zmienione id na name
        if 'name' not in request.data or request.data['name'] == '':
            return Response({
                'message':'Uzytkownik nie zostal odnaleziony.',
                'success':False
            }, status=401)

        query = Profile.objects.filter(name=request.data['id'])
        #new
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

        public_key = RSA.import_key(profile.public_key)
        cipher_rsa = PKCS1_OAEP.new(public_key)

        session_key = get_random_bytes(32)
        auth_key = base58.random(32)

        cache.set(profile.name + '|auth_key', auth_key, 60 * 15)

        profile.session_key = session_key

        # TODO [$609b97d420133e06d703813f]: zaszyfrowany auth_key uzywajac klucza sesji.
        auth_key = cipher_rsa.encrypt(session_key)

        return Response({
            'sessionKey': cipher_rsa.encrypt(session_key),
            'authKey': cipher_rsa.encrypt(auth_key),
            'success': True,
        })


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('name')
    serializer_class = ProfileSerializer


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all().order_by('invite')
    serializer_class = InviteSerializer
