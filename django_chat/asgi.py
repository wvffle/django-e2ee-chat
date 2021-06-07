import os

from channels.db import database_sync_to_async
from channels.sessions import SessionMiddleware, CookieMiddleware
from django.contrib.auth.models import AnonymousUser

import chat.routing

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from chat.models import Profile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_chat.settings')


@database_sync_to_async
def get_user(name):
    try:
        return Profile.objects.get(name=name)
    except Profile.DoesNotExist:
        return None


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # scope['user'] = await get_user(scope["query_string"])
        scope['user'] = None
        return await self.app(scope, receive, send)


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': CookieMiddleware(SessionMiddleware(
        URLRouter(chat.routing.websocket_urlpatterns),
    )),
})
