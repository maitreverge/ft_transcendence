FROM python:3.9-slim

WORKDIR /app

COPY . .

# COPY requirements.txt .

RUN apt update && \ 
	apt upgrade -y && \
	apt install curl -y


RUN pip install --no-cache-dir -r _docker/requirements.txt


# COPY my_entrypoint.sh .

# Copy the whole parent directory


RUN chmod +x _docker/my_entrypoint.sh

ENTRYPOINT ["/bin/sh", "_docker/my_entrypoint.sh"]


# ENTRYPOINT [ "tail", "-f", "/dev/null" ]