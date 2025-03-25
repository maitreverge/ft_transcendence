FROM python:3.11-slim

RUN apt update -y && \ 
	apt upgrade -y && \
	apt install curl -y && \
	apt install postgresql-client -y

WORKDIR /app

COPY _docker/requirements.txt .

# Copy a init list of users + related script
# COPY _docker/user.csv .
# COPY _docker/init_users.py .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# RUN python3 _docker/init_users.py

RUN chmod +x _docker/entrypoint.sh

ENTRYPOINT ["/bin/sh", "_docker/entrypoint.sh"]