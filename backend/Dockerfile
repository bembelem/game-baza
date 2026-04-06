FROM python:3.10-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . /app

ENV PYTHONPATH=/app

CMD uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
EXPOSE 8000