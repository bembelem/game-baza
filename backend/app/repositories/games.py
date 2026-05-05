from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.repositories.mappers.mappers import GameDataMapper
from database.models.games import GameOrm


class GameRepository(BaseRepository):
    model = GameOrm
    mapper = GameDataMapper

    async def get_or_create_batch(self, titles: list[str]) -> dict[str, int]:
        stmt = select(GameOrm.id, GameOrm.normalized_title).where(
            GameOrm.normalized_title.in_(titles)
        )
        result = await self.session.execute(stmt)
        title_to_id = {row.normalized_title: row.id for row in result}

        missing = [t for t in titles if t not in title_to_id]
        if missing:
            new_games = [GameOrm(normalized_title=t, title=t) for t in missing]
            self.session.add_all(new_games)
            await self.session.flush()
            for game in new_games:
                title_to_id[game.normalized_title] = game.id

        return title_to_id