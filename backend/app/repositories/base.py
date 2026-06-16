from typing import Any

from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ObjectAlreadyExistsError
from app.repositories.mappers import DataMapper
from database.database import Base


class BaseRepository:
    """Общая SQL-логика для всех репозиториев.

    `mapper` опционален: если задан - методы возвращают Pydantic-схему;
    если не задан — ORM-объект (для ETL и для справочников).
    """
    model: type[Base]
    mapper: type[DataMapper] | None = None

    def __init__(self, session: AsyncSession):
        self.session = session

    # Read

    async def get_all(self) -> list[Base]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def get_one_or_none(self, **filters) -> Any:
        """Возвращает запись по фильтрам или None.

        Если у репозитория задан mapper - конвертит в Pydantic-схему,
        иначе возвращает ORM-объект.
        """
        result = await self.session.execute(
            select(self.model).filter_by(**filters)
        )
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        if self.mapper is None:
            return obj
        return self.mapper.map_to_domain_entity(obj)

    # Write

    async def add(self, data: BaseModel) -> Any:
        """INSERT с конвертацией результата в Pydantic-схему.

        Требует заданный mapper. На UNIQUE-конфликте бросает
        ObjectAlreadyExistsError с именем нарушенного constraint.
        """
        try:
            stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(stmt)
            obj = result.scalars().one()
            return self.mapper.map_to_domain_entity(obj)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                constraint = getattr(ex.orig.__cause__, "constraint_name", None)
                raise ObjectAlreadyExistsError(constraint=constraint) from ex
            raise

    async def get_or_create(self, **filters) -> Base:
        """Возвращает ORM-запись по фильтрам, создаёт если её нет.

        Не коммитит — flush для получения id, оставляя транзакцию открытой.
        Контроль над session.commit() — за вызывающим кодом.
        """
        result = await self.session.execute(
            select(self.model).filter_by(**filters)
        )
        obj = result.scalar_one_or_none()
        if obj is not None:
            return obj
        obj = self.model(**filters)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def update_by_id(self, item_id: int, fields: dict) -> Any:
        """UPDATE по id, возвращает обновлённую запись (через RETURNING).

        Если задан mapper — конвертит в Pydantic, иначе ORM.
        Возвращает None если записи с таким id нет.
        На UNIQUE-конфликте бросает ObjectAlreadyExistsError.
        """
        try:
            stmt = (
                update(self.model)
                .where(self.model.id == item_id)
                .values(**fields)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            obj = result.scalar_one_or_none()
            if obj is None:
                return None
            if self.mapper is None:
                return obj
            return self.mapper.map_to_domain_entity(obj)
        except IntegrityError as ex:
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                constraint = getattr(ex.orig.__cause__, "constraint_name", None)
                raise ObjectAlreadyExistsError(constraint=constraint) from ex
            raise

    async def delete_by_id(self, item_id: int) -> bool:
        """DELETE по id. Возвращает True если что-то удалилось, иначе False."""
        stmt = delete(self.model).where(self.model.id == item_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0

    async def upsert_batch(
        self,
        rows: list[dict],
        constraint: str,
        skip_cols: tuple[str, ...] = ("id",),
    ) -> None:
        """Bulk INSERT ... ON CONFLICT DO UPDATE.

        Принимает список dict'ов (или Pydantic-схем — но тогда нужно
        заранее вызвать .model_dump()). На конфликте по `constraint`
        обновляет все колонки, кроме перечисленных в `skip_cols`.
        Коммитит транзакцию в конце.
        """
        if not rows:
            return

        table = self.model.__table__

        # 1. Чистим строки от «лишних» ключей. Скрапер кладёт в item служебные
        #    поля (label, item_id, price, activation, details...), которых нет
        #    среди колонок таблицы — иначе pg_insert падает с CompileError
        #    "Unconsumed column names".
        valid_cols = set(table.columns.keys())
        rows = [{k: v for k, v in row.items() if k in valid_cols} for row in rows]

        # 2. Дедуп внутри батча по колонкам конфликтующего constraint'а.
        #    ON CONFLICT DO UPDATE не может задеть одну и ту же строку дважды
        #    в рамках одного INSERT (CardinalityViolationError). Скрапер может
        #    выдать один и тот же товар несколько раз в пределах батча —
        #    оставляем последнее вхождение.
        conflict_cols = self._constraint_columns(constraint)
        if conflict_cols:
            deduped: dict[tuple, dict] = {}
            for row in rows:
                key = tuple(row.get(c) for c in conflict_cols)
                deduped[key] = row  # последнее вхождение побеждает
            rows = list(deduped.values())

        stmt = pg_insert(self.model).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint=constraint,
            set_={
                col.name: stmt.excluded[col.name]
                for col in self.model.__table__.columns
                if col.name not in skip_cols
            },
        )
        await self.session.execute(stmt)
        await self.session.commit()

    def _constraint_columns(self, constraint: str) -> list[str]:
        """Имена колонок UNIQUE-constraint'а по его имени (для дедупа батча).

        Если constraint не найден среди метаданных таблицы — возвращаем []
        (дедуп пропускаем, поведение как раньше).
        """
        for const in self.model.__table__.constraints:
            if const.name == constraint:
                return [col.name for col in const.columns]
        return []
