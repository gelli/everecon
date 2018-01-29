from channels import Group


def ws_connect(message):
    Group('users').add(message.reply_channel)
    message.reply_channel.send({"accept": True})


def ws_disconnect(message):
    Group('users').discard(message.reply_channel)
