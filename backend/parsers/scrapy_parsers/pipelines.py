from app.repositories.raw_offers import RawOfferRepository
from database.database import async_session_maker
from utils.normalizers import normalize_date, normalize_title

class ParserPipeline:
    BATCH_SIZE = 100

    async def open_spider(self, spider):
        self.buffer = []

    async def process_item(self, item, spider):
        item['normalized_title'] = normalize_title(item['title'])
        item['released'] = normalize_date(item.get('released'))
        item['store'] = spider.store_name  # берём из паука
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