from create_bot import bot
import sched
import time


class ChannelCommunicator:
    def parse_datetime(datetime_str):
        parts = datetime_str.split(' ')
        time_parts = parts[0].split(':')
        date_parts = parts[1].split(':')

        hour = int(time_parts[0])
        minute = int(time_parts[1])
        day = int(date_parts[0])
        month = int(date_parts[1])
        year = int(date_parts[2])

        return hour, minute, day, month, year

    async def send_message(channel_id, message):
        if 't.me' in message or 'tg' in message:
            await bot.send_message(channel_id, message, disable_web_page_preview=True)
        else:
            await bot.send_message(channel_id, message)

    async def plan_message(channel_id, message, send_time):
        hour, minute, day, month, year = ChannelCommunicator.parse_datetime(send_time)
