
#!/bin/bash

# Vérifier si un conteneur a été fourni en paramètre
if [ -z "$1" ]; then
  echo "Usage: $0 <nom_du_conteneur>"
  exit 1
fi

CONTAINER_NAME=$1

# Vérifier si le conteneur existe
if ! docker inspect "$CONTAINER_NAME" &>/dev/null; then
  echo "Erreur : Le conteneur '$CONTAINER_NAME' n'existe pas."
  exit 1
fi

# Récupérer la liste des réseaux attachés au conteneur
NETWORKS=$(docker inspect "$CONTAINER_NAME" | jq -r '.[0].NetworkSettings.Networks | keys[]')

# Boucler sur les réseaux pour détacher ceux qui commencent par "network_target_"
for NETWORK in $NETWORKS; do
  if [[ $NETWORK == network_target_* ]]; then
    echo "Détachement du réseau '$NETWORK' du conteneur '$CONTAINER_NAME'..."
    docker network disconnect "$NETWORK" "$CONTAINER_NAME"
    if [ $? -eq 0 ]; then
      echo "Réseau '$NETWORK' détaché avec succès."
    else
      echo "Erreur lors du détachement du réseau '$NETWORK'."
    fi
  fi
done

echo "Traitement terminé."
