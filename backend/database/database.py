from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from database.config import settings

engine_async = create_async_engine(settings.DB_URL_ASYNC, echo=False)

engine_sync = create_engine(settings.DB_URL_SYNC, echo=False)

async_session_maker = async_sessionmaker(bind=engine_async, expire_on_commit=False)

sync_session_maker = sessionmaker(bind=engine_sync, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


# async def test():
#     async with async_session_maker() as session:
#         result = await session.execute(text("SELECT 1"))
#         print(result.fetchall())
# asyncio.run(test())