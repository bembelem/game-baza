# game_baza — backend

## Стек

- **Python 3.12**
- **FastAPI** — REST API
- **PostgreSQL** — база данных
- **SQLAlchemy** — ORM
- **Alembic** — миграции
- **Docker / Docker Compose** — контейнеризация
- **Click** — CLI для управления парсерами

---

## Архитектура

Проект следует **MVC-подходу**:

```
app/
├── models/        # SQLAlchemy модели (M)
├── schemas/       # Pydantic схемы (запросы/ответы)
├── routers/       # FastAPI роутеры (C)
├── services/      # Бизнес-логика
├── repositories/  # Работа с БД
├── parsers/       # ETL-парсеры магазинов
└── cli/           # Click CLI команды
```

---

## Эндпоинты API

### Игры
```
GET  /games               # список игр с фильтрами и пагинацией
GET  /games/{id}          # карточка игры + офферы
```

### Офферы
```
GET  /offers/{id}              # детали оффера
GET  /offers/{id}/price-history # история цен
```

### Аутентификация
```
POST /auth/register        # регистрация
POST /auth/login           # вход, возвращает JWT
```

### Справочники (для фильтров)
```
GET  /platforms            # платформы
GET  /stores               # магазины
GET  /genres               # жанры
```

### Пользователи
```
GET  /users/{id}                      # публичный профиль
GET  /users/{id}/wishlist             # вишлист пользователя
GET  /users/me                        # свой профиль
PATCH  /users/me                      # изменить профиль
DELETE /users/me                      # удалить свой профиль
POST   /users/me/wishlist/{game_id}   # добавить игру в вишлист
DELETE /users/me/wishlist/{game_id}   # убрать игру из вишлиста
```

### Отзывы
```
GET  /games/{id}/reviews   # отзывы к игре
POST /games/{id}/reviews   # оставить отзыв (требует auth)
```

---

## Схема БД

Основные таблицы: `games`, `offers`, `price_history`, `users`, `reviews`, `wishlists`, `stores`, `developers`, `publishers`, `genres`, `platforms`.

Связующие таблицы many-to-many: `genres_games`, `platforms_games`.

> Полная ER-диаграмма: [https://dbdiagram.io/d/game-baza-69b743ae78c6c4bc7aeb5304](#) 

---

## Запуск

### Через Docker Compose

```bash
docker-compose up --build
```

### Локально

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload
```

Документация API доступна по адресу: `http://localhost:8000/docs`

---

## Переменные окружения

Создай файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/game_baza
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Парсеры

Парсеры запускаются через CLI и пишут данные напрямую в БД через upsert.

```bash
python -m app.cli parse --store steambuy
python -m app.cli parse --store gabestore
python -m app.cli parse --all
```

---

