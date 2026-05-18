from sqlalchemy import String, Integer, ForeignKey, Text, Table, Column
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database.database import Base

genres_games = Table(
    'genres_games',
    Base.metadata,
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True)
)

platforms_games = Table(
    'platforms_games',
    Base.metadata,
    Column('platform_id', Integer, ForeignKey('platforms.id', ondelete='CASCADE'), primary_key=True),
    Column('game_id', Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True)
)


class StoreOrm(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True)

    offers: Mapped[list["OfferOrm"]] = relationship(back_populates="store")


class PlatformOrm(Base):
    __tablename__ = "platforms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    games: Mapped[list["GameOrm"]] = relationship(
        secondary=platforms_games,
        back_populates="platforms"
    )


class GenreOrm(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    games: Mapped[list["GameOrm"]] = relationship(
        secondary=genres_games,
        back_populates="genres"
    )


class DeveloperOrm(Base):
    __tablename__ = "developers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    games: Mapped[list["GameOrm"]] = relationship(back_populates="developer")


class PublisherOrm(Base):
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    games: Mapped[list["GameOrm"]] = relationship(back_populates="publisher")