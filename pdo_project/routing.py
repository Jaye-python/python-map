from django.urls import re_path
from channels.auth import AuthMiddlewareStack

from map import consumers

#channels var socket = new WebSocket('ws://localhost:8000/ws/livesignals/');
websocket_urlpatterns = [
    re_path(r'ws/livesignals/', consumers.SignalConsumer.as_asgi()),
]

