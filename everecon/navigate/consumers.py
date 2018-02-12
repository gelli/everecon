from channels.consumer import AsyncConsumer


class WebSocketConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print('connected')
        await self.channel_layer.group_add('users', self.channel_name)
        await self.send({
            "type": "websocket.accept",
        })

        await self.channel_layer.group_send("users", {
            'type': 'users.message',
            'text': 'hello world'
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard("users", self.channel_name)

    async def users_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event["text"]
        })
