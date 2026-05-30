# Bruk en offisiell og lett Python-base
FROM python:3.11-slim

# Sett arbeidskatalogen inni containeren
WORKDIR /app

# Installer systemavhengigheter hvis nødvendig (f.eks. for raskere nettverk)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer Python-pakkene vi trenger direkte
RUN pip install --no-cache-dir fastapi uvicorn requests pydantic

# Kopier resten av analyse-koden inn i containeren
COPY . .

# Åpne porten som FastAPI kjører på
EXPOSE 8000

# Kommandoen som starter analyseserveren

