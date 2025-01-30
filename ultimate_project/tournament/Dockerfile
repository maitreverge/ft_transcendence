FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "tournament.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]


