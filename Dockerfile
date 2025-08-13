# Dockerfile
FROM python:3.11-slim

# System deps for pandas/matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libatlas-base-dev libfreetype6-dev libpng-dev \
    fonts-dejavu-core tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code (sessions + common)
COPY sessions/ /app/sessions/
COPY common/ /app/common/

# Default command: run Session 1 using a CSV under data/
# (You can override it at runtime)
CMD ["python", "sessions/01_histogramas/main.py", "--csv", "data/categoria_de_corredores.csv"]