# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: dan <dan@student.42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/01/29 13:35:00 by seblin            #+#    #+#              #
#    Updated: 2025/01/29 21:15:10 by dan              ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all:
	-docker-compose up --build -d
	
clean:
	-docker stop $$(docker ps -qa)
	-docker rm $$(docker ps -qa)
	-docker volume rm $$(docker volume ls -q)
	-echo y | docker network rm $$(docker network ls -q)
	rm -rf staticfiles/*

re: clean all

