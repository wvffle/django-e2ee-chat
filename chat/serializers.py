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


class RegisterSerializer(serializers.Serializer):
    invite = serializers.CharField()
    public_key = serializers.CharField()
    hcaptcha = serializers.CharField()

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key in list(validated_data):
            instance[key] = validated_data[key]
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key in list(validated_data):
            instance[key] = validated_data[key]
        instance.save()
        return instance
