FROM python:3.11-slim

# Minimal system deps for matplotlib fonts & tzdata
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY common/ /app/common/
COPY sessions/ /app/sessions/

# script
CMD ["python", "sessions/01_histogramas/Histogramas_Python.py", "--csv", "data/categoria_de_corredores.csv"]