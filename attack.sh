#!/bin/bash

# Adresse IP du serveur (localhost dans ce cas)
SERVER="http://127.0.0.1:8080"

# Nombre de requêtes à envoyer
REQUESTS=10  # Modifiez ce nombre selon vos besoins

# Boucle pour envoyer les requêtes
for ((i=1; i<=REQUESTS; i++)); do
    curl -s $SERVER > /dev/null &
done

# Attendre que tous les processus se terminent
wait
