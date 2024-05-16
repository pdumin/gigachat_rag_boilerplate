# Используем официальный образ Python 3.11 в качестве базового
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Скопируем файлы requirements.txt в рабочую директорию
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем все файлы приложения в рабочую директорию
COPY . .

# Устанавливаем переменную окружения для Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true

# Открываем порт, который будет использовать Streamlit
EXPOSE 8501

# Запускаем приложение
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
