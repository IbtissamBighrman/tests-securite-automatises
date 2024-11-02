#!/bin/bash

# Pinger l'adresse IP du conteneur cible
while true; do
    ping -c 4 172.29.0.2  # Adresse IP du conteneur target_container
    sleep 5  # Attendre 5 secondes avant de pinguer à nouveau
done
