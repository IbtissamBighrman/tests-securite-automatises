#!/bin/bash

# Vérifier si les paramètres sont passés
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <NETWORK_NAME> <NEW_SUBNET> <CONTAINER_NAME>"
  exit 1
fi

# Variables
NETWORK_NAME=$1          # Nom du réseau
NEW_SUBNET=$2            # Nouveau sous-réseau
CONTAINER_NAME=$3        # Nom du conteneur

# Vérifier si le réseau existe déjà
EXISTING_NETWORK=$(docker network ls --filter name=^${NETWORK_NAME}$ --format "{{.Name}}")

if [ "$EXISTING_NETWORK" == "$NETWORK_NAME" ]; then
  echo "Le réseau $NETWORK_NAME existe déjà. Suppression du réseau..."
  
  # Déconnecter le conteneur du réseau avant de le supprimer
  echo "Déconnexion du conteneur $CONTAINER_NAME du réseau $NETWORK_NAME..."
  docker network disconnect $NETWORK_NAME $CONTAINER_NAME
  
  # Supprimer le réseau
  docker network rm $NETWORK_NAME
else
  echo "Le réseau $NETWORK_NAME n'existe pas. Création d'un nouveau réseau."
fi

# Créer un nouveau réseau avec le sous-réseau spécifié
echo "Création du réseau $NETWORK_NAME avec le sous-réseau $NEW_SUBNET..."
docker network create --driver bridge --subnet $NEW_SUBNET $NETWORK_NAME

# Connecter le conteneur au réseau
echo "Connexion du conteneur $CONTAINER_NAME au réseau $NETWORK_NAME..."
docker network connect $NETWORK_NAME $CONTAINER_NAME

# Vérifier l'adresse IP attribuée dynamiquement
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_NAME)
echo "Le conteneur $CONTAINER_NAME a l'adresse IP $CONTAINER_IP sur le réseau $NETWORK_NAME."

echo "Le script est terminé."
