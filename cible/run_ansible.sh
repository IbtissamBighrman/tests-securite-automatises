#!/bin/bash

echo "Choisissez une option :"
echo "1. Créer un conteneur cible et l'associer à un sous-réseau"
echo "2. Ajouter une cible dans un réseau existant"
read -p "Entrez votre choix (1 ou 2) : " choice

if [ "$choice" == "1" ]; then
  # Demander les paramètres pour l'option 1
  read -p "Veuillez entrer le chemin vers le répertoire contenant le Dockerfile : " dockerfile_path
  read -p "Veuillez entrer l'ID de la machine cible : " id_cible
  read -p "Veuillez entrer le sous-réseau pour le conteneur (par exemple, 192.168.1.0/24) : " subnet

  # Exécuter uniquement les tâches liées à l'option 1
  ansible-playbook -i inventory playbook.yml \
    -e "dockerfile_path=$dockerfile_path id_cible=$id_cible subnet=$subnet" \
    --tags "create_container"

elif [ "$choice" == "2" ]; then
  # Demander les paramètres pour l'option 2
  read -p "Veuillez entrer le nom du réseau existant : " network_name
  read -p "Veuillez entrer l'adresse IP de la cible : " target_ip

  # Exécuter uniquement les tâches liées à l'option 2
  ansible-playbook -i inventory playbook.yml \
    -e "network_name=$network_name target_ip=$target_ip" \
    --tags "add_target"

else
  echo "Choix invalide. Veuillez exécuter le script à nouveau et entrer 1 ou 2."
  exit 1
fi
