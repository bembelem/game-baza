from app.repositories.raw_offers import RawOfferRepository
from database.database import async_session_maker
from utils.normalizers import normalize_date, normalize_title

STEAM_STORE_NAME = "steam"

# class ParserPipeline:
#     BATCH_SIZE = 100
#
#     def open_spider(self, spider):
#         self.buffer = []
#         self.steam_store_id = None
#         asyncio.run(self._init_async())
#
#     async def _init_async(self):
#         async with async_session_maker() as session:
#             steam_store = await session.execute(
#                 select(StoreOrm).where(StoreOrm.name == STEAM_STORE_NAME)
#             )
#             steam_store = steam_store.scalar_one_or_none()
#             if steam_store:
#                 self.steam_store_id = steam_store.id
#
#     def process_item(self, item, spider):
#         normalized_title = normalize_title(item['title'])
#         self.buffer.append(OfferCreate(
#             **item,
#             store_id=self.steam_store_id,
#             normalized_title=normalize_title(normalized_title),
#             game_id=self._resolve_game_id(normalized_title)
#         ))
#         if len(self.buffer) >= self.BATCH_SIZE:
#             asyncio.run(self._push_batch())
#         return item
#
#     def close_spider(self, spider):
#         if self.buffer:
#             asyncio.run(self._push_batch())
#
#     async def _push_batch(self):
#         async with async_session_maker() as session:
#             repo = OfferRepository(session)
#             await repo.add_batch(self.buffer)
#         self.buffer.clear()
#
#     async def _resolve_game_id(self, normalized_title: str) -> int | None:
#         async with async_session_maker() as session:
#             repo = OfferRepository(session)
#             game_id = await repo.get_id_by_normalized_title(normalized_title)
#             return game_id


STEAM_STORE_NAME = "steam"

class ParserPipeline:
    BATCH_SIZE = 100

    async def open_spider(self, spider):
        self.buffer = []

    async def process_item(self, item, spider):
        item['normalized_title'] = normalize_title(item['title'])
        item['released'] = normalize_date(item['released'])
        item['store'] = STEAM_STORE_NAME
        self.buffer.append(item)
        if len(self.buffer) >= self.BATCH_SIZE:
            await self._push_batch()
        return item

    async def close_spider(self, spider):
        if self.buffer:
            await self._push_batch()

    async def _push_batch(self):
        async with async_session_maker() as session:
            repo = RawOfferRepository(session)
            await repo.add_batch(self.buffer)
        self.buffer.clear()