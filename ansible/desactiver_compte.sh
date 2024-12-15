#!/bin/bash

# Vérifier si un id_container a été passé en paramètre
if [ -z "$1" ]; then
  echo "Erreur : Vous devez fournir un id_container en paramètre."
  echo "Usage : $0 <id_container>"
  exit 1
fi

# Récupérer l'ID du conteneur depuis le paramètre
container_id="$1"

# Nom de l'utilisateur à désactiver (fixe pour ce script)
username="client1"

# Désactiver le mot de passe de l'utilisateur dans le conteneur
docker exec -it "$container_id" passwd -l "$username"

# Tuer toutes les sessions SSH actives de cet utilisateur
docker exec -it "$container_id" pkill -u "$username" sshd

# Afficher un message de confirmation
echo "L'utilisateur $username a été désactivé et déconnecté immédiatement dans le conteneur $container_id. Il ne peut plus se connecter via SSH."
