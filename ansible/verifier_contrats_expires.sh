#!/bin/bash
echo "$(date) - Début de l'exécution du script" >> /var/log/cron_script.log
# Configuration de la connexion à la base de données
DB_HOST="mysql-container"
DB_USER="root"
DB_PASSWORD="rootpassword"
DB_NAME="containers_db"

# Vérifier les contrats expirés
EXPIRED_CONTRACTS=$(mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -se "
SELECT c.container_id
FROM contract AS co
JOIN container AS c ON co.contract_id = c.contract_id
WHERE co.end_datetime < NOW() AND co.status = 'active';
")

# Si des contrats expirés sont trouvés
if [ ! -z "$EXPIRED_CONTRACTS" ]; then
  for CONTAINER_ID in $EXPIRED_CONTRACTS; do
    # Exécuter le script avec l'ID du conteneur comme paramètre
    ./desctiver_compte.sh "$CONTAINER_ID"
    
    # Mettre à jour le statut du contrat à 'expired'
    mysql -u "$DB_USER" -p"$DB_PASSWORD" -h "$DB_HOST" -D "$DB_NAME" -e "
    UPDATE contract 
    SET status = 'expired' 
    WHERE contract_id = (
        SELECT contract_id 
        FROM container 
        WHERE container_id = '$CONTAINER_ID'
    );
    "
  done
fi
echo "$(date) - Fin de l'exécution du script" >> /var/log/cron_script.log
