from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from auth_data import BOT_TOKEN, PROXY_URL

# bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
