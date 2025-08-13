# Lightweight Python base image
FROM python:3.11-slim

# System deps for pandas/matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libatlas-base-dev libfreetype6-dev libpng-dev \
    fonts-dejavu-core tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Default command (can be overridden at runtime)
CMD ["python", "src/histograms.py", "--csv", "data/categoria_de_corredores.csv"]