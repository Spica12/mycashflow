# Образ Python
FROM python:3.13-slim

# Встановлюємо змінні оточення:
# PYTHONUNBUFFERED=1 змушує Python одразу виводити логи в консоль (корисно для FastAPI)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# COPY requirements.txt /app/requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# COPY /src /app/src
# COPY main.py /app/main.py
COPY ./src ./src
COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
