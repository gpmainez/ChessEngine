
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy do to working directory (/app_)
COPY . .
EXPOSE 8000

#webapp on uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
