#!/bin/bash

# Configuration de la connexion à la base de données
DB_HOST="mysql-container"
DB_USER="root"
DB_PASSWORD="rootpassword"
DB_NAME="containers_db"

# Journalisation
LOG_FILE="/var/log/cleanup_damaged_containers.log"
echo "$(date) - Début de l'exécution du script" >> "$LOG_FILE"

# Fonction pour vérifier si un conteneur Docker est actif
is_container_active() {
    CONTAINER_NAME=$1
    docker ps --format '{{.Names}}' | grep -w "$CONTAINER_NAME" &> /dev/null
    return $?
}

# Récupérer les conteneurs de la BDD
CONTAINERS=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
SELECT container_id, container_name 
FROM container;
")

# Parcourir chaque conteneur récupéré
while IFS=$'\t' read -r CONTAINER_ID CONTAINER_NAME; do
    echo "Traitement du conteneur : ID=$CONTAINER_ID, Nom=$CONTAINER_NAME" >> "$LOG_FILE"

    # Vérifier si le conteneur est actif dans Docker
    if is_container_active "$CONTAINER_NAME"; then
        echo "Le conteneur $CONTAINER_NAME est actif. Aucun traitement nécessaire." >> "$LOG_FILE"
    else
        echo "Le conteneur $CONTAINER_NAME est endommagé ou inactif." >> "$LOG_FILE"

        # Supprimer le conteneur Docker (s'il existe toujours, mais arrêté)
        if docker ps -a --format '{{.Names}}' | grep -w "$CONTAINER_NAME" &> /dev/null; then
            docker rm -f "$CONTAINER_NAME" >> "$LOG_FILE" 2>&1
            echo "Conteneur $CONTAINER_NAME supprimé du système Docker." >> "$LOG_FILE"
        fi

        # Supprimer l'entrée du conteneur dans la BDD
        mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -e "
        DELETE FROM container WHERE container_id = '$CONTAINER_ID';
        " >> "$LOG_FILE" 2>&1
        echo "Conteneur $CONTAINER_NAME supprimé de la base de données." >> "$LOG_FILE"
    fi
done <<< "$CONTAINERS"

echo "$(date) - Fin de l'exécution du script" >> "$LOG_FILE"
