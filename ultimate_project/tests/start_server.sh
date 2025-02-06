#!/bin/bash

# Démarrage du serveur
echo "Starting the server..."
make clean > /dev/null 2>&1
make re > /dev/null 2>&1 &  # Lance le serveur en arrière-plan

# Attente que les containers Docker soient en cours d'exécution
echo "Waiting for Docker containers to be ready..."
until docker ps --filter "name=ctn_nginx" --filter "status=running" | grep -q "ctn_nginx"; do
    sleep 1
done
echo "Docker containers are up and running!"
