FROM python:3.14-slim
WORKDIR /app
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
# COPY ./app /app/app
CMD ["sh", "-c", "while true; do echo 'service is running'; sleep 5; done"]