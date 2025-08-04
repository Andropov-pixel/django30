# Этап сборки приложения
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

# Этап сервера

# позволяет использовать все обновления и исправления, присутствующие в последнем выпуске Nginx
FROM nginx:latest

COPY --from=builder /app /app

# копируем файл конфигурации в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# копируем статические файлы вебсайта в директорию обслуживания
COPY html/ /usr/share/nginx/html/

# открываем порт 80 для http трафика
EXPOSE 80