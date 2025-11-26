FROM python:3.14-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install --no-root

# Copy application code
COPY web ./web

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with Uvicorn
CMD ["uvicorn", "web.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
