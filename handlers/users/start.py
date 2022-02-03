from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api.crud import create_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await create_user(
            name=message.from_user.first_name,
            surname=message.from_user.last_name,
        )
    except Exception as err:
        print(err)
    await message.answer(f'Пользователь {message.from_user.first_name} сохранен в бд')


print('Start loaded')