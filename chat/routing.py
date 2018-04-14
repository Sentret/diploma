from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/messages/<room_name>', consumers.ChatConsumer),
]