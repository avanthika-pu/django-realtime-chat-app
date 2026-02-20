import os
import django
from django.core.asgi import get_asgi_application

# 1. Set the settings module BEFORE anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 2. Initialize Django
django.setup()

# 3. Import your routing and other channels parts AFTER django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})