from rest_framework import serializers
from .models import Profile, Invite


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'invite')


class InviteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invite
        fields = ('invite',)
