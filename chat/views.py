from django.shortcuts import render
from rest_framework import viewsets
from chat.models import Profile, Invite
from chat.serializers import ProfileSerializer, InviteSerializer


def index(request):
    return render(request, 'chat/index.html', context={
        # 'error': True,
        # 'statusCode': 500,
        # 'message': 'test message'
    })


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('name')
    serializer_class = ProfileSerializer


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all().order_by('invite')
    serializer_class = InviteSerializer
