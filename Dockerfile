FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* /app/
RUN uv sync

COPY . /app

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]