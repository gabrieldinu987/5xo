# ==========================================
# Base Image
# ==========================================

FROM python:3.12-slim

# ==========================================
# Environment
# ==========================================
# evită generarea fișierelor *.pyc
ENV PYTHONDONTWRITEBYTECODE=1

# face ca logurile să apară imediat în docker logs
ENV PYTHONUNBUFFERED=1

# ==========================================
# Working Directory
# ==========================================

WORKDIR /app

# ==========================================
# Install dependencies
# ==========================================

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Copy application
# ==========================================

COPY . .

# ==========================================
# Network
# ==========================================

EXPOSE 5000

# ==========================================
# Start application
# ==========================================

CMD ["python", "app.py"]