FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY config.py .
COPY api.py .
COPY chroma_db/ chroma_db/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
