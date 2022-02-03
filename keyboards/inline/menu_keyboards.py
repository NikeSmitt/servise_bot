from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_api import crud
from utils.db_api.models import Item

menu_cd = CallbackData('show_menu', 'level', 'category', 'subcategory', 'item_id')
buy_item_cd = CallbackData('buy', 'item_id')


def make_callback_data(level: int, category: str = '0', subcategory: str = '0', item_id: int = 0):
    return menu_cd.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard():
    current_level = 0
    
    markup = InlineKeyboardMarkup()
    
    item_categories = await crud.get_categories()
    
    for category in item_categories:
        item_quantity = await crud.count_items(category.category_code)
        button_text = f'{category.category_name} ({item_quantity} шт)'
        callback_data = make_callback_data(current_level + 1, category.category_code)
        
        markup.insert(InlineKeyboardButton(
            text=button_text,
            callback_data=callback_data
        ))
    
    return markup


async def subcategories_keyboard(category: str):
    current_level = 1
    markup = InlineKeyboardMarkup()
    
    item_subcategories = await crud.get_subcategories(category)
    print(item_subcategories)
    for subcategory in item_subcategories:
        item_quantity = await crud.count_items(subcategory.category_code, subcategory.subcategory_code)
        button_text = f'{subcategory.subcategory_name} ({item_quantity} шт)'
        callback_data = make_callback_data(level=current_level + 1,
                                           category=subcategory.category_code,
                                           subcategory=subcategory.subcategory_code)
        
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=make_callback_data(level=current_level - 1))
    )
    
    return markup


async def items_keyboard(category, subcategory):
    current_level = 2
    markup = InlineKeyboardMarkup()
    
    items = await crud.get_items(category, subcategory)
    print(f'{category=}, {subcategory=}')
    print(f'{items=}')
    
    for item in items:
        button_text = f"{item.name} - {item.price}"
        callable_data = make_callback_data(level=current_level + 1,
                                           category=category,
                                           subcategory=subcategory,
                                           item_id=item.id)
        
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callable_data)
        )
    
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=make_callback_data(level=current_level - 1, category=category))
    )
    
    return markup


async def item_keyboard(category, subcategory, item_id):
    current_level = 3
    markup = InlineKeyboardMarkup()
    
    markup.row(
        InlineKeyboardButton(
            text=f'Купить',
            callback_data=buy_item_cd.new(item_id=item_id)
        )
    )
    
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=make_callback_data(level=current_level - 1, category=category))
    )
    
    return markup
