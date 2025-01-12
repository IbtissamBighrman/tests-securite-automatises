#!/bin/bash

# Vérification du nombre de paramètres
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <nom_du_reseau> <nom_du_conteneur>"
  exit 1
fi

# Récupération des paramètres
NETWORK_NAME="$1"
CONTAINER_NAME="$2"

# Vérification si le réseau existe
if ! docker network inspect "$NETWORK_NAME" > /dev/null 2>&1; then
  echo "Erreur : Le réseau '$NETWORK_NAME' n'existe pas."
  exit 1
fi

# Vérification si le conteneur existe
if ! docker inspect "$CONTAINER_NAME" > /dev/null 2>&1; then
  echo "Erreur : Le conteneur '$CONTAINER_NAME' n'existe pas."
  exit 1
fi

# Associer le conteneur au réseau
docker network connect "$NETWORK_NAME" "$CONTAINER_NAME"

if [ $? -eq 0 ]; then
  echo "Le conteneur '$CONTAINER_NAME' a été ajouté au réseau '$NETWORK_NAME' avec succès."
else
  echo "Erreur : Impossible d'ajouter le conteneur '$CONTAINER_NAME' au réseau '$NETWORK_NAME'."
  exit 1
fi
