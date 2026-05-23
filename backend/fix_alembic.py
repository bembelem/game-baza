"""Разовый фикс: руками сбросить указатель alembic_version на существующую ревизию.

Используется когда БД ссылается на ревизию, файла которой нет в migrations/versions/.
Запуск:
    uv run python fix_alembic.py
"""
import asyncio
from sqlalchemy import text

from database.database import async_session_maker

NEW_HEAD = "e93b71b10d8b"  # ← существующий head из `alembic heads`


async def main() -> None:
    async with async_session_maker() as session:
        await session.execute(text("DELETE FROM alembic_version"))
        await session.execute(
            text("INSERT INTO alembic_version (version_num) VALUES (:v)"),
            {"v": NEW_HEAD},
        )
        await session.commit()
        print(f"alembic_version → {NEW_HEAD}")


if __name__ == "__main__":
    asyncio.run(main())
