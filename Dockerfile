# Imagine de bază
FROM python:3.12-slim

# Directorul de lucru din container
WORKDIR /app

# Copiem fișierul cu dependențe
COPY requirements.txt .

# Instalăm dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Copiem aplicația
COPY . .

# Expunem portul Flask
EXPOSE 5000

# Variabile de mediu
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Pornim aplicația
CMD ["python", "app.py"]