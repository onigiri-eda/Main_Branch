# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y \
	libpq-dev \
	gcc \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/
COPY database/init.sql /docker-entrypoint-initdb.d/

CMD ["python", "almass.py"]