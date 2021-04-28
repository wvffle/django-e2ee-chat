import json

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django_chat.settings import HCAPTCHA_SECRET
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from chat.utils import base58
from chat.models import Profile, Invite
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

        if HCAPTCHA_SECRET is not "":
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

        for profile in Profile.objects.all():
            if profile.public_key == request.data['public_key']:
                return Response({
                    'success': False,
                    'message': 'Taki użytkownik już istnieje.'
                }, status=403)

        name = base58.random(8)
        profile = Profile(
            invite=query.get(),
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
        # answer = {
        #     'sessionKey': "....",
        #     'authKey': "....",
        #     'success': True,
        # }
        return Response({"test": request.data['id']})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('name')
    serializer_class = ProfileSerializer


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all().order_by('invite')
    serializer_class = InviteSerializer
