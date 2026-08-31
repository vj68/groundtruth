FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app
COPY fixtures ./fixtures
COPY static ./static
COPY templates ./templates

RUN pip install --no-cache-dir .
RUN mkdir -p /app/artifacts/runs /app/local-data

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
