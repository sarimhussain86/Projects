"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# application = get_asgi_application()


# chatapp/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.contrib.staticfiles.handlers import StaticFilesHandler  # to serve static files in development
import chats.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

# django_asgi_app = get_asgi_application()  # to serve static files in development

application = ProtocolTypeRouter({
    'http': get_asgi_application(), #   used for productions,
    # 'http': StaticFilesHandler(django_asgi_app),  # Serve static files in development
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    ),
})