# PDF Compressor (cleaned)

Simple FastAPI service that accepts a PDF upload and returns a compressed PDF using Ghostscript.

## Run locally

Make sure you have Ghostscript installed (`gs` on PATH).

Install deps:
```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

Build:
```
docker build -t pdf-compressor:latest .
docker run -p 8000:8000 pdf-compressor:latest
```
