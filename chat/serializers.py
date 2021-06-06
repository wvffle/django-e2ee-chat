from rest_framework import serializers
from .models import Profile, Invite, Room


class DummySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'invite')


class InviteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invite
        fields = ('invite',)


class RegisterSerializer(DummySerializer):
    invite = serializers.CharField()
    public_key = serializers.CharField()
    hcaptcha = serializers.CharField()


class LoginSerializer(DummySerializer):
    name = serializers.CharField()


class LoginVerifySerializer(DummySerializer):
    authKey = serializers.CharField()


class RoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    image = serializers.ImageField()
    display_name = serializers.CharField()

    class Meta:
        model = Room
        fields = ('name', 'display_name', 'image')
