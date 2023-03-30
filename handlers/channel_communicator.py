from create_bot import bot


class ChannelCommunicator:
    async def send_message(channel_id, message):
        await bot.send_message(channel_id, message)
