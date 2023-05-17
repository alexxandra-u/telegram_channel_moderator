from aiogram.utils import executor
from create_bot import dp, bot
from handlers.database_communicator import DatabaseCommunicator
from handlers.user_communicator import UserCommunicator
from dotenv import load_dotenv, find_dotenv
import nltk


async def on_startup(_):
    DatabaseCommunicator.sql_start()
    load_dotenv(find_dotenv())
    nltk.download('movie_reviews')
    nltk.download("punkt")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
