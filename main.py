from aiogram.utils import executor
from create_bot import dp, bot
from handlers.database_communicator import DatabaseCommunicator
from handlers.user_communicator import UserCommunicator
from dotenv import load_dotenv, find_dotenv


async def on_startup(_):
    DatabaseCommunicator.sql_start()
    load_dotenv(find_dotenv())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
