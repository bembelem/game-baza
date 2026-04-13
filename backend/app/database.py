from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


# async def test():
#     async with async_session_maker() as session:
#         result = await session.execute(text("SELECT 1"))
#         print(result.fetchall())
# asyncio.run(test())