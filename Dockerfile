FROM python:3.12-slim

WORKDIR /app

# system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# poetry
RUN pip install --no-cache-dir poetry

# dependency cache layer
COPY pyproject.toml poetry.lock ./

# disable venv inside container
RUN poetry config virtualenvs.create false

# install only runtime deps (ВАЖНО)
RUN poetry install --no-interaction --no-root --only main

# app source
COPY . .

# entrypoint permissions
RUN chmod +x docker/entrypoint.sh

# better logging
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

ENTRYPOINT ["sh", "docker/entrypoint.sh"]

CMD ["run"]
