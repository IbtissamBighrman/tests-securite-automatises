#!/bin/bash

# Demander le nom du conteneur Docker
read -p "Entrez le nom ou l'ID du conteneur Docker: " container_name

# Demander le nom de l'utilisateur à réactiver
read -p "Entrez le nom de l'utilisateur à réactiver: " username

# Réactiver le mot de passe de l'utilisateur (annuler le verrouillage)
docker exec -it "$container_name" passwd -u "$username"

# Redéfinir le mot de passe si nécessaire
# docker exec -it "$container_name" bash -c "echo '$username:newpassword' | chpasswd"

# Afficher un message de confirmation
echo "L'utilisateur $username a été réactivé dans le conteneur $container_name et peut maintenant se connecter via SSH."
