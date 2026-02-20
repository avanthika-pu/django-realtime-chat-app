from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Add .as_asgi() to both routes
    re_path(r"ws/status/$", consumers.ChatConsumer.as_asgi()), 
    re_path(r"ws/chat/(?P<username>\w+)/$", consumers.ChatConsumer.as_asgi()),
]