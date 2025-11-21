FROM python:3.11-slim
LABEL org.opencontainers.image.source=https://github.com/bakhta11/pdf-compressor-clean




RUN apt-get update && apt-get install -y --no-install-recommends \
    ghostscript \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
