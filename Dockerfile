FROM python:3.12-slim

WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY backend/ ./backend/

# Устанавливаем рабочую директорию
WORKDIR /app/backend

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
