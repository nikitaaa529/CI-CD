# Этап 1: установка зависимостей в отдельное виртуальное окружение
FROM python:3.12-slim AS builder
WORKDIR /build
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Этап 2: минимальный runtime-образ, приложение работает не от root
FROM python:3.12-slim AS runtime
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser
COPY --from=builder /opt/venv /opt/venv
COPY app.py .
RUN mkdir -p /app/data && chown -R appuser:appgroup /app
USER appuser
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
 
