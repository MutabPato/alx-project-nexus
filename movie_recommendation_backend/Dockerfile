# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /.

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev curl build-essential && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Run migrations and start server
CMD ["gunicorn", "movie_recommendation_backend.wsgi:application", "--bind", "0.0.0.0:8000"]