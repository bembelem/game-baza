from database.database import sync_session_maker

from sqlalchemy import select

from database.models.games import GameOrm

with sync_session_maker() as session:
    query = select(GameOrm).where(GameOrm.title == "Cyberpunk 2077")
    result = session.execute(query)
    result1 = result.scalar()
    breakpoint()
