from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu_keyboards import categories_keyboard, menu_cd, subcategories_keyboard, items_keyboard, \
    item_keyboard
from loader import dp
from utils.db_api.crud import get_item


@dp.message_handler(Command('menu'))
async def show_meny(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_keyboard()
    
    if isinstance(message, Message):
        await message.answer('Что мы можем предложить', reply_markup=markup)
    
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: types.CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category, subcategory)
    await callback.message.edit_reply_markup(markup)


async def show_item(callback: types.CallbackQuery, category, subcategory, item_id):
    markup = await item_keyboard(category, subcategory, item_id)
    
    item = await get_item(item_id)
    text = f'Купи {item.name}'
    await callback.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    category = callback_data.get('category')
    subcategory = callback_data.get('subcategory')
    item_id = int(callback_data.get('item_id'))
    
    print(current_level, category, subcategory)
    
    level_func = {
        "0": list_categories,  # Отдаем категории
        "1": list_subcategories,  # Отдаем подкатегории
        "2": list_items,  # Отдаем товары
        "3": show_item  # Предлагаем купить товар
    }
    
    current_level_func = level_func[current_level]
    await current_level_func(
        call,
        category=category,
        subcategory=subcategory,
        item_id=item_id
    )
