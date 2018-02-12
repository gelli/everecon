from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from everecon.navigate import consumers

print("routing loaded")

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        url('^live/$', consumers.WebSocketConsumer),
    ])
})
