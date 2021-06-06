from django.contrib import admin
from django import forms

from chat.models import Profile, Invite, Ban, Room


class InviteForm(forms.ModelForm):
    invite = forms.CharField(max_length=8, min_length=8)

    class Meta:
        model = Invite
        fields = ['invite']


class InviteAdmin(admin.ModelAdmin):
    form = InviteForm


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'invite')
    list_filter = ('invite',)
    search_fields = ('name', 'invite')
    exclude = ('session_key', 'public_key')
    readonly_fields = ('name', 'invite')


class BanAdmin(admin.ModelAdmin):
    list_display = ('invite', 'profile')
    list_filter = ('invite',)


admin.site.register(Invite, InviteAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Ban, BanAdmin)
admin.site.register(Room)
