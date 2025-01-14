#!/bin/bash 

# Vérifiez si un contract_id a été fourni en argument
if [ -z "$1" ]; then
    echo "Usage: $0 <contract_id>"
    exit 1
fi

CONTRACT_ID=$1

# Informations de connexion à la base de données
DB_HOST="mysql-container"
DB_USER="root"
DB_PASSWORD="rootpassword"
DB_NAME="containers_db"

# Récupérer les conteneurs liés au contrat
CONTAINERS=$(mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME -se "
    SELECT container_name 
    FROM container 
    WHERE contract_id = $CONTRACT_ID;
")

# Vérifiez si des conteneurs sont associés au contrat
if [ -z "$CONTAINERS" ]; then
    echo "Aucun conteneur associé au contrat ID: $CONTRACT_ID"
    exit 1
fi

# Récupérer le nom du réseau lié au contrat
NETWORK_NAME=$(mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME -se "
    SELECT t.network_name 
    FROM contract c 
    JOIN target t ON c.target_id = t.target_id 
    WHERE c.contract_id = $CONTRACT_ID;
")

# Vérifiez si un réseau est associé au contrat
if [ -z "$NETWORK_NAME" ]; then
    echo "Aucun réseau associé au contrat ID: $CONTRACT_ID"
    exit 1
fi

echo "Contrat ID: $CONTRACT_ID"
echo "Réseau cible: $NETWORK_NAME"
echo "Conteneurs associés :"
echo "$CONTAINERS"

# Déconnecter les conteneurs de leurs réseaux actuels
for CONTAINER in $CONTAINERS; do
    echo "Déconnexion du conteneur: $CONTAINER"
    ./network_disconnect.sh "$CONTAINER"
done

# Connecter les conteneurs au nouveau réseau
for CONTAINER in $CONTAINERS; do
    echo "Connexion du conteneur: $CONTAINER au réseau: $NETWORK_NAME"
    ./network_connect.sh "$NETWORK_NAME" "$CONTAINER"
done

# Exécuter le script envoyer_mail.py
echo "Envoi d'un e-mail concernant l'opération"
python3 envoyer_mail.py "$CONTRACT_ID"
if [ $? -eq 0 ]; then
    echo "E-mail envoyé avec succès."
else
    echo "Erreur lors de l'envoi de l'e-mail."
fi

# Exécuter le script auto_connexion.py
echo "Exécution du script d'auto-connexion"
python3 auto_connexion.py 
if [ $? -eq 0 ]; then
    echo "Auto-connexion terminée avec succès."
else
    echo "Erreur lors de l'exécution du script d'auto-connexion."
fi

echo "Opération terminée."
