FROM python:3.14-slim AS base

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN uv sync --frozen --no-dev

CMD ["uv", "run", "uvicorn", "willimakeit.main:app", "--host", "0.0.0.0", "--port", "8000"]