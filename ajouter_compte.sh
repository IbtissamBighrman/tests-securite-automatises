#!/bin/bash

# Demander le nom du conteneur Docker où l'utilisateur sera ajouté
read -p "Entrez le nom ou l'ID du conteneur Docker: " container_name

# Demander le nom du nouvel utilisateur
read -p "Entrez le nom du nouvel utilisateur: " username

# Créer l'utilisateur dans le conteneur et lui attribuer un shell bash
docker exec -it "$container_name" useradd -m -s /bin/bash "$username"

# Définir un mot de passe pour l'utilisateur dans le conteneur
docker exec -it "$container_name" bash -c "echo '$username:password' | chpasswd"

# Ajouter l'utilisateur au groupe 'clients' dans le conteneur
docker exec -it "$container_name" usermod -aG clients "$username"

# Appliquer les restrictions : interdire 'useradd' et 'adduser' via sudo
docker exec -it "$container_name" bash -c "echo '$username ALL=(ALL) NOPASSWD: ALL, !/usr/sbin/useradd, !/usr/sbin/adduser' > /etc/sudoers.d/$username"
docker exec -it "$container_name" bash -c "chmod 0440 /etc/sudoers.d/$username"

# Vérifier que l'utilisateur a bien été ajouté au groupe 'clients'
docker exec -it "$container_name" groups "$username"

# Afficher un message de confirmation
echo "L'utilisateur $username a été ajouté avec succès au groupe 'clients' dans le conteneur $container_name."

# Optionnel : afficher les détails de l'utilisateur
docker exec -it "$container_name" chage -l "$username"
