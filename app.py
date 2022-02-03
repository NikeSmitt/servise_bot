from aiogram import executor

from utils.db_api.add_to_db import add_to_db

from loader import dp
import handlers
from utils.db_api.crud import del_all_items
from utils.db_api.db_helper import init_db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    
    # Инициализируем сессию и создаем таблицы в бд
    await init_db()
    
    # await del_all_items()
    
    # await add_to_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

