FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app
COPY requirements-lock.txt .
RUN pip install --no-cache-dir -r requirements-lock.txt
COPY src ./src

EXPOSE 5000
CMD ["sh", "-c", "cd src && gunicorn app:app --bind 0.0.0.0:${PORT} --timeout 120"]
