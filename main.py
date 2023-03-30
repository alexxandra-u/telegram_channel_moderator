from aiogram.utils import executor
from create_bot import dp
from handlers.database_communicator import DatabaseCommunicator


async def on_startup(_):
    DatabaseCommunicator.sql_start()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
