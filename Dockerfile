FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN pip install --no-cache-dir --upgrade pip

# Copy dependency files
COPY pyproject.toml /app/

# Install Python dependencies
RUN pip install \
    django \
    djangorestframework \
    djangorestframework-simplejwt \
    celery \
    redis \
    psycopg[binary] \
    python-dotenv \
    requests \
    gunicorn \
    django-celery-beat

# Copy project code
COPY . /app

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]