FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml ./
COPY src ./src
COPY tests ./tests

RUN pip install --no-cache-dir ".[dev]"

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "greenwheels_mcp"]
