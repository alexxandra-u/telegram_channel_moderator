import requests
import uuid
import datetime
import time
from handlers.database_communicator import DatabaseCommunicator
from auth_data import VK_PARSING_TOKEN
version = 5.92

class VkParser:
    async def parse_vk(source, user_id, parse_time):
        domain = source[1][15:]
        now = datetime.datetime.now()
        now_unixtime = time.mktime(now.timetuple())
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': VK_PARSING_TOKEN,
                                    'v': version,
                                    'domain': domain
                                })
        posts = response.json()['response']['items']
        for post in posts:
            if now_unixtime - post["date"] < int(parse_time) and post["marked_as_ads"] == 0:
                post_id = str(uuid.uuid4()).replace('-', '')
                post_link = "https://vk.com/" + domain + "?w=wall" + str(post["from_id"]) + "_" + str(post["id"])
                text = post["text"]
                date = post["date"]
                post_object = [post_id, user_id, "vk", source[1], post_link, text, date]
                await DatabaseCommunicator.sql_add_content(post_object)

