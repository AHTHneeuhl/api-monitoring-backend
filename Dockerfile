FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv
RUN uv sync

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]