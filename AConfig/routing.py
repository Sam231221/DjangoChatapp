import MChat.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            MChat.routing.websocket_urlpatterns
        )
    )
})