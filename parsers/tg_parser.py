from handlers.database_communicator import DatabaseCommunicator
from telethon.sync import TelegramClient
from utils.language_analyser import Analyser
import datetime
import time
import uuid
import os


class TgParser:
    def check_time(time_str, parse_time):
        post_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
        post_unixtime = int(post_time.timestamp())
        now_time = datetime.now()
        now_unixtime = time.mktime(now_time.timetuple())
        if now_unixtime - post_unixtime < int(parse_time):
            return True, post_unixtime
        else:
            return False, post_unixtime

    async def parse_tg(source, user_id, parse_time):
        phone = os.getenv('PHONE')
        api_id_tg = os.getenv('API_ID_TG')
        api_hash_tg = os.getenv('API_HASH_TG')
        client = TelegramClient(phone, int(api_id_tg), api_hash_tg)
        await client.start()
        channel = await client.get_entity(source[1])
        messages = await client.get_messages(channel, limit=50)
        for mes in messages:
            post_time = mes.date
            post_unixtime = int(post_time.timestamp())
            now_time = datetime.datetime.now()
            now_unixtime = time.mktime(now_time.timetuple())
            if now_unixtime - post_unixtime < int(parse_time):
                post_id = str(uuid.uuid4()).replace('-', '')
                text = mes.text
                tone = Analyser.get_tone(text)
                post_object = [post_id, user_id, "tg", source[1], source[1], text, post_unixtime, tone]
                await DatabaseCommunicator.sql_add_content(post_object)
            else:
                break
        await client.disconnect()

