from create_bot import bot

class ChannelCommunicator:
    async def send_message(channel_id, message):
        if 't.me' in message or 'tg' in message:
            await bot.send_message(channel_id, message, disable_web_page_preview=True)
        else:
            await bot.send_message(channel_id, message)
