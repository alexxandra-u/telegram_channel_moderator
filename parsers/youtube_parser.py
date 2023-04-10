from auth_data import YOUTUBE_PARSING_TOKEN
from handlers.database_communicator import DatabaseCommunicator
import requests
import re
import json
import uuid
import time
import urllib
from datetime import datetime
from bs4 import BeautifulSoup


class YoutubeParser:
    def check_time(time_str, parse_time):
        post_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')
        post_unixtime = int(post_time.timestamp())
        now_time = datetime.now()
        now_unixtime = time.mktime(now_time.timetuple())
        if now_unixtime - post_unixtime < int(parse_time):
            return True, post_unixtime
        else:
            return False, post_unixtime

    async def parse_youtube(source, user_id, parse_time):
        channel_link = source[1]
        r = requests.get(channel_link)
        soup = BeautifulSoup(r.content, 'html.parser')
        data = soup.find_all('meta', property="al:ios:url")[0].attrs["content"]
        channel_id = re.search(r'/(?<=channel\/)[\w-]+', data).group(0)[1:]

        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

        first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(
            YOUTUBE_PARSING_TOKEN, channel_id)

        url = first_url
        inp = urllib.request.urlopen(url)
        resp = json.load(inp)

        for i in resp['items']:
            is_new, post_unixtime = YoutubeParser.check_time(i['snippet']['publishTime'], parse_time)
            if i['id']['kind'] == "youtube#video" and is_new:
                post_id = str(uuid.uuid4()).replace('-', '')
                post_link = base_video_url + i['id']['videoId']
                text = i['snippet']['title']
                date = post_unixtime
                post_object = [post_id, user_id, "youtube", source[1], post_link, text, date]
                await DatabaseCommunicator.sql_add_content(post_object)
            elif not is_new:
                break
