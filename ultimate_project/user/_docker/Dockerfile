FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt update && \ 
	apt upgrade -y && \
	apt install curl -y


RUN pip install --no-cache-dir -r requirements.txt


COPY entrypoint.sh .

# Copy the whole parent directory
COPY ../ .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
