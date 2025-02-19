# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: flverge <flverge@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/01/29 13:35:00 by seblin            #+#    #+#              #
#    Updated: 2025/02/19 16:41:48 by flverge          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: install_compose create_volume
	-docker compose up --build

prod: install_compose clean 
	-docker compose -f docker-compose.yml up --build

clean:
	-docker stop $$(docker ps -qa)
	-docker rm $$(docker ps -qa)
# -docker rmi $$(docker images -qa)
	-docker volume rm $$(docker volume ls -q)
	-echo y | docker network rm $$(docker network ls -q)
	rm -rf staticfiles/*

re: clean all

prune:
	docker system prune --all --force

install_compose:
	@sudo apt-get install docker-compose-plugin

create_volume:
	@echo "\n\033[1;33m***| Creating PostgreSQL Volumes |***\033[0m\n"
	@sudo mkdir -p /home/volumes_transcendence/postgres
	@echo "\n\033[1;32m***| PostgreSQL Volumes Created |***\033[0m\n"

# Using this rule actually deletes the DB. Run it at your own risks.
delete_volume:
	@echo "\n\033[1;33m***| Deleting PostgreSQL volumes |***\033[0m\n"
	@sudo rm -rf /home/volumes_transcendence/postgres
	@echo "\n\033[1;32m***| PostgreSQL Volumes Deteted |***\033[0m\n"

.PHONY: all prod clean re install_compose

# all:
# 	docker-compose up

# build:
# 	docker-compose build

# prod: clean 
# 	docker-compose -f docker-compose.yml up

# clean:
# 	-docker-compose down -v
# 	rm -rf staticfiles/*

# re: clean build all