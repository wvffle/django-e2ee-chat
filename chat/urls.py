from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework import routers
from chat import views
from django_chat import settings
from django_chat.settings import DEBUG

router = routers.DefaultRouter()
router.register(r'v1/profiles', views.ProfileViewSet)
router.register(r'v1/invites', views.InviteViewSet)
router.register(r'v1/register', views.RegisterViewSet, basename='v1/register')
router.register(r'v1/login', views.LoginViewSet, basename='v1/login')
router.register(r'v1/login/verify', views.LoginVerifyViewSet, basename='v1/login/verify')
router.register(r'v1/profile/rooms', views.ProfileRoomsViewSet, basename='v1/profile/rooms')
router.register(r'v1/messages', views.MessagesViewSet, basename='v1/messages')
router.register(r'v1/room/invite', views.RoomInviteViewSet, basename='v1/room/invite')

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if DEBUG:
    from django.views.decorators.csrf import csrf_exempt
    from proxy.views import proxy_view

    @csrf_exempt
    def proxy(request, path):
        remote_url = 'http://localhost:3001/' + path
        return proxy_view(request, remote_url, {})

    urlpatterns.append(url('(?P<path>chat/public/.*)', proxy))
    urlpatterns.append(url('(?P<path>__vite_ping)', proxy))
    urlpatterns.append(url('(?P<path>@windicss-devtools-update)', proxy))

urlpatterns.append(url('.*', views.index, name='index'))
