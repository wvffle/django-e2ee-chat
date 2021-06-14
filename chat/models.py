from django.contrib.auth.models import User
from django.db import models


class Invite(models.Model):
    id = models.AutoField(primary_key=True)
    invite = models.CharField(max_length=8)

    def __str__(self):
        return self.invite


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE)
    name = models.CharField(max_length=8)
    session_key = models.CharField(max_length=1024)
    public_key = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='admin')
    participants = models.ManyToManyField(Profile)
    name = models.CharField(max_length=8)
    display_name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='room_images', default='1px-transparent.gif')

    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.IntegerField()
    message = models.JSONField()
    retention_seconds = models.IntegerField()


class Ban(models.Model):
    id = models.AutoField(primary_key=True)
    invite = models.OneToOneField(Invite, on_delete=models.CASCADE, null=True, blank=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def is_banned(self, profile):
        return profile == self.profile or profile.invite == self.invite

    def __str__(self):
        if self.invite:
            return 'invite-' + str(self.invite)

        return 'profile-' + str(self.profile)
