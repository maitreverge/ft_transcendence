FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles

RUN python manage.py collectstatic --noinput


CMD ["uvicorn", "static_files.asgi:application", "--host", "0.0.0.0", "--port", "8001", "--reload"]

