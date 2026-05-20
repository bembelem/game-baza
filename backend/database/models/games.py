from datetime import date

from sqlalchemy import String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base
from database.models.catalogs import platforms_games, genres_games, GenreOrm, PlatformOrm, PublisherOrm, DeveloperOrm, \
    StoreOrm


class GameOrm(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), unique=True)
    normalized_title: Mapped[str] = mapped_column(String(500), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    release_date: Mapped[date | None] = mapped_column(index=True)
    image_url: Mapped[str | None] = mapped_column(String(1000))

    developer_id: Mapped[int | None] = mapped_column(ForeignKey('developers.id', ondelete='SET NULL'))
    developer: Mapped["DeveloperOrm"] = relationship(back_populates="games")

    publisher_id: Mapped[int | None] = mapped_column(ForeignKey('publishers.id', ondelete='SET NULL'))
    publisher: Mapped["PublisherOrm"] = relationship(back_populates="games")

    platforms: Mapped[list["PlatformOrm"]] = relationship(
        secondary=platforms_games,
        back_populates="games"
    )
    genres: Mapped[list["GenreOrm"]] = relationship(
        secondary=genres_games,
        back_populates="games"
    )
    offers: Mapped[list["OfferOrm"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan"
    )

class OfferOrm(Base):
    __tablename__ = 'offers'
    __table_args__ = (
        UniqueConstraint("title", "store_id", name="uq_game_store"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    normalized_title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    released: Mapped[date | None]
    image_url: Mapped[str | None] = mapped_column(String(1000))
    link: Mapped[str | None] = mapped_column(String(1000))
    reviews_count: Mapped[int | None]
    positive_percent: Mapped[int | None]

    game_id: Mapped[int] = mapped_column(ForeignKey('games.id', ondelete='CASCADE'), index=True)
    game: Mapped["GameOrm"] = relationship(back_populates="offers")

    store_id: Mapped[int | None] = mapped_column(ForeignKey('stores.id', ondelete='SET NULL'), index=True)
    store: Mapped["StoreOrm"] = relationship(back_populates="offers")

    developer: Mapped[str | None] = mapped_column(String(255))
    publisher: Mapped[str | None] = mapped_column(String(255))
    platforms: Mapped[str | None] = mapped_column(Text)
    genres: Mapped[str | None] = mapped_column(Text)

    store_game_link: Mapped[str | None] = mapped_column(String(1000))
    price_original: Mapped[int | None]
    price_discount: Mapped[int | None] = mapped_column(index=True)
    discount_percent: Mapped[str | None] = mapped_column(String(4))


class RawOfferOrm(Base):
    __tablename__ = 'raw_offers'
    __table_args__ = (
        UniqueConstraint("title", "store", name="uq_raw_offer_store"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    store: Mapped[str] = mapped_column(String(100))
    normalized_title: Mapped[str] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    released: Mapped[date | None]
    image_url: Mapped[str | None] = mapped_column(String(1000))
    link: Mapped[str | None] = mapped_column(String(1000))
    reviews_count: Mapped[int | None]
    positive_percent: Mapped[int | None]
    developer: Mapped[str | None] = mapped_column(String(255))
    publisher: Mapped[str | None] = mapped_column(String(255))
    genres: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    platforms: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    price_original: Mapped[str | None]
    price_discount: Mapped[str | None]
    discount_percent: Mapped[str | None] = mapped_column(String(4))
    is_processed: Mapped[bool] = mapped_column(default=False)
