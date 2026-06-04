# obraz bazowy - lekki python
FROM python:3.12-slim

# katalog roboczy w kontenerze
WORKDIR /app

# kopiuj tylko requirements najpierw (cache warstwy)
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn

# kopiuj reszte projektu
COPY engine/ ./engine/
COPY static/ ./static/
COPY main.py .

# port fastapi
EXPOSE 8000

# uruchom serwer
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
