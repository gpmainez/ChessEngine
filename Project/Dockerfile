# Uzywamy oficjalnego, odchudzonego obrazu Pythona 3.11
FROM python:3.11-slim

# Zmienne srodowiskowe zapobiegajace tworzeniu .pyc i buforowaniu logow
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Kopiujemy zaleznosci i instalujemy
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy reszte kodu projektu
COPY . .

# Eksponujemy port serwera FastAPI
EXPOSE 8000

# Uruchomienie produkcyjnego serwera ASGI Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
