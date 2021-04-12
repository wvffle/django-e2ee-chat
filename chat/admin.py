from django.contrib import admin
from django import forms

from chat.models import Profile, Invite, Ban


class InviteForm(forms.ModelForm):
    invite = forms.CharField(max_length=8, min_length=8)

    class Meta:
        model = Invite
        fields = ['invite']


class InviteAdmin(admin.ModelAdmin):
    form = InviteForm


admin.site.register(Invite, InviteAdmin)

# TODO [$6073b33e0ec279062172ac28]: Make Profile readonly
# TODO [$6073b33e0ec279062172ac29]: Hide public key and session key
admin.site.register(Profile)
admin.site.register(Ban)
