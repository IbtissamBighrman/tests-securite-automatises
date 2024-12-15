#!/bin/bash

TARGET="172.28.0.2"

# Lancer des pings continuellement vers la cible
while true; do
    ping -c 4 "$TARGET"  # Envoie 4 paquets de ping vers la cible
    sleep 5               # Pause de 5 secondes entre chaque envoi de pings
done
