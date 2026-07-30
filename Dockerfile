FROM python:3.13-slim

LABEL maintainer="Gabriel Dinu"
LABEL application="5XO"

# compilare python in byte code la prima rulare a aplicatiei, pentru a imbunatati performanta
ENV PYTHONDONTWRITEBYTECODE=1
# setare valoarea la 1 asigura output  python strout and strerr trimise in terminal
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD curl -f http://localhost:5000 || exit 1

CMD ["python3", "app.py"]