from app.repositories.base import BaseRepository
from database.models.games import RawOfferOrm


class RawOfferRepository(BaseRepository):
    """Хранилище сырых офферов от скрапера."""
    model = RawOfferOrm

    async def add_batch(self, raw_offers: list[dict]) -> None:
        """Обёртка над `BaseRepository.upsert_batch` с зашитым UNIQUE-constraint'ом и полями,
        которые не перезаписываем."""

        await self.upsert_batch(
            raw_offers,
            constraint="uq_raw_offer_store",
            skip_cols=("id", "title", "store"),
        )
