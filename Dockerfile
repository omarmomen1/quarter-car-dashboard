FROM python:3.12-slim

WORKDIR /app

# System deps for scipy/numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching)
COPY requirements-backend.txt ./
RUN pip install --no-cache-dir -r requirements-backend.txt

COPY src/ ./src/
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

CMD uvicorn suspensionlab.backend.api.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2
