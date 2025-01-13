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

# Récupérer les conteneurs de la BDD avec leur contract_id
CONTAINERS=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
SELECT container_id, container_name, contract_id 
FROM container;
")

# Parcourir chaque conteneur récupéré
while IFS=$'\t' read -r CONTAINER_ID CONTAINER_NAME CONTRACT_ID; do
    # Nettoyage du nom du conteneur pour retirer un '/' au début
    CLEANED_CONTAINER_NAME=$(echo "$CONTAINER_NAME" | sed 's/^\/\+//')

    echo "Traitement du conteneur : ID=$CONTAINER_ID, Nom=$CLEANED_CONTAINER_NAME, Contract ID=$CONTRACT_ID" >> "$LOG_FILE"

    # Vérifier si le conteneur est actif dans Docker
    if is_container_active "$CLEANED_CONTAINER_NAME"; then
        echo "Le conteneur $CLEANED_CONTAINER_NAME est actif. Aucun traitement nécessaire." >> "$LOG_FILE"
    else
        echo "Le conteneur $CLEANED_CONTAINER_NAME est endommagé ou inactif." >> "$LOG_FILE"

        # Supprimer le conteneur Docker (s'il existe toujours, mais arrêté)
        if docker ps -a --format '{{.Names}}' | grep -w "$CLEANED_CONTAINER_NAME" &> /dev/null; then

            # Vérifier si le contrat associé au conteneur est 'active'
            CONTRACT_STATUS=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
                SELECT status
                FROM contract
                WHERE contract_id = $CONTRACT_ID;
            ")
            echo "Status du contrat associé : $CONTRACT_STATUS" >> "$LOG_FILE"
            
            # Si le contrat est actif, chercher un conteneur libre et actif
            if [ "$CONTRACT_STATUS" == "active" ]; then
                echo "Le contrat associé au conteneur $CLEANED_CONTAINER_NAME est actif." >> "$LOG_FILE"

                # Récupérer tous les conteneurs libres
                FREE_CONTAINERS=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
                    SELECT container_id, container_name 
                    FROM container 
                    WHERE contract_id IS NULL;
                ")

                # Parcourir les conteneurs libres pour trouver un conteneur actif
                FOUND_ACTIVE_CONTAINER=false
                while IFS=$'\t' read -r FREE_CONTAINER_ID FREE_CONTAINER_NAME; do
                    CLEANED_FREE_CONTAINER_NAME=$(echo "$FREE_CONTAINER_NAME" | sed 's/^\/\+//')

                    # Vérifier si le conteneur est actif
                    if is_container_active "$CLEANED_FREE_CONTAINER_NAME"; then
                        echo "Conteneur libre et actif trouvé : ID=$FREE_CONTAINER_ID, Nom=$CLEANED_FREE_CONTAINER_NAME" >> "$LOG_FILE"
                        FOUND_ACTIVE_CONTAINER=true

                        # Remplacer contract_id dans la base de données
                        if mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
                            UPDATE container 
                            SET contract_id = '$CONTRACT_ID' 
                            WHERE container_id = '$FREE_CONTAINER_ID';
                        "; then
                            echo "Le contract_id du conteneur $CLEANED_FREE_CONTAINER_NAME a été remplacé par $CONTRACT_ID." >> "$LOG_FILE"
                        else
                            echo "Erreur lors de la mise à jour du contract_id pour le conteneur $CLEANED_FREE_CONTAINER_NAME." >> "$LOG_FILE"
                        fi

                         # Mettre à jour le contract_id du conteneur endommagé à NULL
                        if mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
                            UPDATE container 
                            SET contract_id = NULL 
                            WHERE container_id = '$CONTAINER_ID';
                        "; then
                            echo "Le contract_id du conteneur endommagé $CLEANED_CONTAINER_NAME a été mis à NULL." >> "$LOG_FILE"
                        else
                            echo "Erreur lors de la mise à NULL du contract_id pour le conteneur $CLEANED_CONTAINER_NAME." >> "$LOG_FILE"
                        fi

                        # Une fois un conteneur actif trouvé et utilisé, arrêter la recherche
                        break
                    fi
                done <<< "$FREE_CONTAINERS"

                # Si aucun conteneur libre et actif n'est trouvé
                if [ "$FOUND_ACTIVE_CONTAINER" = false ]; then
                    echo "Aucun conteneur libre et actif trouvé pour remplacer le contract_id." >> "$LOG_FILE"
                fi
            else
                echo "Le contrat associé au conteneur $CLEANED_CONTAINER_NAME n'est pas actif. Aucune action entreprise." >> "$LOG_FILE"
            fi
        else
            echo "Le conteneur $CLEANED_CONTAINER_NAME n'existe pas ou ne peut pas être supprimé." >> "$LOG_FILE"
        fi
    fi
done <<< "$CONTAINERS"

echo "$(date) - Fin de l'exécution du script" >> "$LOG_FILE"
