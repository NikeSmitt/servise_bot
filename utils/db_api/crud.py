from typing import Tuple, List

from utils.db_api.database import async_db_session
from utils.db_api.models import User, Item
from sqlalchemy import select, distinct, and_, delete, func


async def create_user(**kwargs):
    user = User(**kwargs)
    async_db_session.add(user)
    await async_db_session.commit()


async def add_item(**kwargs):
    new_item = Item(**kwargs)
    async_db_session.add(new_item)
    await async_db_session.commit()
    return new_item


async def get_categories() -> List[Item]:
    categories = await async_db_session.execute(select(Item).distinct(Item.category_code))
    return [value[0] for value in categories.all()]


async def get_subcategories(category: str) -> List[Item]:
    result = await async_db_session.execute(select(Item)
                                            .distinct(Item.subcategory_code)
                                            .where(Item.category_code == category))
    return [value[0] for value in result.all()]


async def count_items(category_code: str, subcategory_code: str = None) -> int:
    conditions = [Item.category_code == category_code]
    
    if subcategory_code is not None:
        conditions.append(Item.subcategory_code == subcategory_code)
    
    total = await async_db_session.execute(select(func.count()).select_from(select(Item).where(and_(*conditions))))
    return total.scalar_one()


async def get_items(category_code: str = None, subcategory_code: str = None) -> List[Item]:
    conditions = []
    
    if category_code is not None:
        conditions.append(Item.category_code == category_code)
    if subcategory_code is not None:
        conditions.append(Item.subcategory_code == subcategory_code)
    
    result = await async_db_session.execute(select(Item).where(and_(*conditions)))
    return [value[0] for value in result.all()]


async def get_item(item_id: int) -> Item:
    result = await async_db_session.execute(select(Item).where(Item.id == item_id))
    
    return result.first()[0]


async def del_all_items():
    await async_db_session.execute(delete(Item))
    await async_db_session.commit()
