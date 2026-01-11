# ------------------------------
# Base image
# ------------------------------
FROM python:3.14-slim

WORKDIR /app

# ------------------------------
# Install system dependencies
# ------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    libmagic-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# ------------------------------
# Install Poetry
# ------------------------------
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry

# ------------------------------
# Copy only dependency files
# ------------------------------
COPY pyproject.toml poetry.lock ./

# ------------------------------
# Install dependencies
# ------------------------------
RUN poetry install --no-root


# ------------------------------
# Development command: uvicorn in reload mode
# ------------------------------
CMD ["python", "worker.py"]
