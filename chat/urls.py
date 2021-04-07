from django.urls import path
from chat import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
]