import os
env = os.environ
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from map import consumers

from pdo_project import routing

settings_file = 'local' if env.get('IS_LOCAL') else 'production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdo_project.settings.' + settings_file)

#channels
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})