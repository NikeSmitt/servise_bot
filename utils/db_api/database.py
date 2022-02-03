import asyncio
from typing import Union

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from data.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self):
        self._session: Union[Session, None] = None
        self._engine: Union[Engine, None] = None
    
    def __getattr__(self, name):
        return getattr(self._session, name)
    
    async def init(self):
        self._engine = create_async_engine(
            f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
            echo=True
        )
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()
    
    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


async_db_session = AsyncDatabaseSession()





# if __name__ == '__main__':
#     async def async_main():
#         await async_db_session.init()
#         await async_db_session.create_all()
#
#
#     asyncio.run(async_main())
