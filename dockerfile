# Base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for building mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    netcat-openbsd \
    libmariadb-dev \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Copy wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


# Expose port
EXPOSE 8000

CMD ["gunicorn", "CRM.wsgi:application", "--bind", "0.0.0.0:8000"]