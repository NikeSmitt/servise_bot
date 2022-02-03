import asyncio

from utils.db_api.database import async_db_session
from .models import User
from .crud import create_user


async def init_db():
    await async_db_session.init()
    await async_db_session.create_all()
    
    # await create_user(name='Nikita', surname='Alikov', middle_name='Astrahanovich')


# asyncio.run(async_main())
