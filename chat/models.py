from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Invite(models.Model):
    invite = models.CharField(max_length=8)


class Profile(models.Model):
    invite = models.ForeignKey(Invite, on_delete=models.CASCADE)
    name = models.CharField(max_length=8)
    session_key = models.CharField(max_length=32)
    public_key = models.CharField(max_length=1024)

    @receiver(post_save, sender=User)
    def create_user_profile(self, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(self, instance, **kwargs):
        instance.profile.save()


class Room(models.Model):
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    message = models.JSONField()
    retention_seconds = models.IntegerField()


class Ban(models.Model):
    invite = models.OneToOneField(Invite, on_delete=models.CASCADE, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
