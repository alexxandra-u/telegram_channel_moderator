from auth_data import phone, API_ID_TG, API_HASH_TG
from handlers.database_communicator import DatabaseCommunicator
from telethon.sync import TelegramClient
import datetime
import time
import uuid

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
        client = TelegramClient(phone, API_ID_TG, API_HASH_TG)
        await client.start()
        channel = await client.get_entity(source[1])
        messages = await client.get_messages(channel, limit=50)
        # print(1)
        for mes in messages:
            post_time = mes.date
            post_unixtime = int(post_time.timestamp())
            now_time = datetime.datetime.now()
            now_unixtime = time.mktime(now_time.timetuple())
            if now_unixtime - post_unixtime < int(parse_time):
                post_id = str(uuid.uuid4()).replace('-', '')
                text = mes.text
                post_object = [post_id, user_id, "tg", source[1], source[1], text, post_unixtime]
                await DatabaseCommunicator.sql_add_content(post_object)
            else:
                break
        await client.disconnect()

