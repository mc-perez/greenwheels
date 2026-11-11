FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml ./
RUN pip install --no-cache-dir ".[dev]"

COPY app ./app
COPY tests ./tests
COPY alembic.ini ./
COPY alembic ./alembic
COPY scripts ./scripts

RUN chmod +x scripts/entrypoint.sh

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["scripts/entrypoint.sh"]
