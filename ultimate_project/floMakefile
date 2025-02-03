# docker-compose up --build -> Build Docker image from DockerFile + create container + start them
all:
	@echo "\n\033[1;33m***| BUILDING AND UP-ING CONTAINERS ⌛ |***\033[0m\n"
	@docker-compose up --build -d
	@echo "\n\033[1;32m***| CONTAINERS BUILT AND RUNNING ✅ |***\033[0m\n"

# docker-compose up -> Create + Start container
up:
	@echo "\n\033[1;33m***| UP-ING CONTAINERS ⌛ |***\033[0m\n"
	@docker-compose up --detach
	@echo "\n\033[1;32m***| CONTAINERS UP ✅ |***\033[0m\n"

# docker-compose down -> Stops and removes containers
down:
	@echo "\n\033[1;33m***| DOWNING CONTAINERS ⌛ |***\033[0m\n"
	@docker-compose down
	@echo "\n\033[1;32m***| CONTAINERS DOWN ✅ |***\033[0m\n"

# docker-compose down -v -> Stops and removes containers + remove volumes created by the docker-compose
hard_down:
	@echo "\n\033[1;33m***| HARD-DOWNING CONTAINERS ⌛ |***\033[0m\n"
	@docker-compose down -v
	@echo "\n\033[1;32m***| CONTAINERS HARD-DOWNED ✅ |***\033[0m\n"

# docker-compose stop -> Stops a container without removing it
stop:
	@echo "\n\033[1;33m***| STOPPING CONTAINERS ⌛ |***\033[0m\n"
	@docker-compose stop
	@echo "\n\033[1;32m***| CONTAINERS STOPPED ✅ |***\033[0m\n"

# docker-compose start -> Start existing containers
start:
	@echo "\n\033[1;33m***| STARTING CONTAINERS ⌛ |***\033[0m\n"
	@docker-compose start
	@echo "\n\033[1;32m***| CONTAINERS STARTED ✅ |***\033[0m\n"

# Need to double $$ for shell substitution
delete_images:
	@echo "\n\033[1;33m***| DELETING DOCKER IMAGES ⌛ |***\033[0m\n"
	@docker rmi $$(docker images -a -q)
	@echo "\n\033[1;32m***| DOCKER IMAGES DELETED ✅ |***\033[0m\n"

restart: stop start

soft_clean: down

re : soft_clean all

# Deletes Containers + volumes + images
medium_clean: down delete_image

# Deletes everything, including your soul
hard_clean: down
	@echo "\n\033[1;33m***| CLEANNING CONTAINERS |***\033[0m\n"
	@docker system prune --all --force
	@echo "\n\033[1;32m***| FULL DOCKER CLEANED |***\033[0m\n"

#! Rule to implement
create_volume:
	@echo "\n\033[1;33m***| Creating Volumes --RULE TO ME IMPLEMENTED-- |***\033[0m\n"
	@echo "\n\033[1;32m***| Volumes Created --RULE TO ME IMPLEMENTED-- |***\033[0m\n"

# Permanently delete all volumes ! Use with caution
delete_volume:
	@echo "\n\033[1;33m***| Deleting volumes |***\033[0m\n"
	@docker volume rm $(docker volume ls -q)
	@echo "\n\033[1;32m***| Volumes Deteted |***\033[0m\n"

.PHONY : all up down hard_down stop start delete_images restart softclean mediumclean hard_clean create_volume delete_volume