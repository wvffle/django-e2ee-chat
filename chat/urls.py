from django.urls import path, include
from rest_framework import routers
from chat import views

router = routers.DefaultRouter()
router.register(r'profiles', views.ProfileViewSet)
router.register(r'invites', views.InviteViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
