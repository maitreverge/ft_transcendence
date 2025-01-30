FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/staticfiles

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
# CMD ["uvicorn", "static_files.asgi:application", "--host", "0.0.0.0", "--port", "8001", "--reload"]
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8001"]