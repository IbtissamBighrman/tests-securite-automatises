try:
    import pymysql
except ImportError:
    print("La bibliothèque pymysql est requise. Veuillez l'installer avec la commande suivante : pip install pymysql")

try:
    import paramiko

except ImportError:
    print("La bibliothèque pymysql est requise. Veuillez l'installer avec la commande suivante : pip install paramiko")


# Informations de connexion
DB_HOST = "127.0.0.1" # Nom du conteneur ou IP
DB_PORT = 3306               # Port exposé par MySQL
DB_USER = "root"             # Utilisateur
DB_PASSWORD = "rootpassword" # Mot de passe
DB_NAME = "containers_db"    # Base de données





def connect_to_db():
    """
    Connexion à la base de données MySQL.

    Cette fonction tente de se connecter à une base de données MySQL en utilisant les
    informations de connexion fournies (hôte, port, utilisateur, mot de passe, nom de la base de données).
    En cas de succès, elle retourne l'objet de connexion. En cas d'échec, elle affiche un message d'erreur
    et des suggestions pour résoudre le problème, puis retourne None.

    Returns:
        connection (pymysql.connections.Connection or None): L'objet de connexion à la base de données
        si la connexion est réussie, sinon None.

    Raises:
        pymysql.MySQLError: Si une erreur survient lors de la tentative de connexion à la base de données.

    Exemple:
        >>> connection = connect_to_db()
        Tentative de connexion à la base de données my_database sur localhost:3306...
        Connexion réussie à la base de données.
    """
    """Connexion à la base de données MySQL."""
    try:
        print(f"Tentative de connexion à la base de données {DB_NAME} sur {DB_HOST}:{DB_PORT}...")
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Connexion réussie à la base de données.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        print("Suggestions :")
        print("- Vérifiez si le conteneur MySQL est en cours d'exécution (docker ps).")
        print("- Assurez-vous que le conteneur est accessible via son nom ou son adresse IP.")
        print("- Assurez-vous que le port 3306 est exposé et accessible.")
        return None





def check_contract_status(contract_id: int) -> str:
    """
    Vérifie le statut d'un contrat.

    Cette fonction se connecte à la base de données, exécute une requête pour vérifier le statut
    d'un contrat en fonction de son ID, et retourne le statut du contrat.

    Args:
        contract_id (int): L'ID du contrat à vérifier.

    Returns:
        str: Le statut du contrat si trouvé, sinon None.
    """
    connection = connect_to_db()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            # Requête pour vérifier le statut du contrat
            sql_query = "SELECT status FROM contract WHERE contract_id = %s"
            cursor.execute(sql_query, (contract_id,))
            result = cursor.fetchone()
            
            if result:
                status = result[0]
                print(f"Statut du contrat {contract_id} : {status}")
                return status
            else:
                print(f"Aucun contrat trouvé avec l'ID {contract_id}.")
                return None
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return None
    finally:
        connection.close()



def get_container_info(container_id):
    """Récupère les informations détaillées sur un conteneur spécifique."""
    connection = connect_to_db()
    if not connection:
        return
    
    try:
        with connection.cursor() as cursor:
            # Requête pour récupérer les informations du conteneur
            sql_query = """
            SELECT c.container_id, c.container_name, c.ssh_port, c.image, c.mdp_tmp, con.start_datetime, con.end_datetime, con.status
            FROM container c
            LEFT JOIN contract con ON c.contract_id = con.contract_id
            WHERE c.container_id = %s;
            """
            cursor.execute(sql_query, (container_id,))
            result = cursor.fetchone()

            if result:
                container_info = {
                    'container_id': result[0],
                    'container_name': result[1],
                    'ssh_port': result[2],
                    'image': result[3],
                    'mdp_tmp': result[4],
                    'start_datetime': result[5],
                    'end_datetime': result[6],
                    'status': result[7]
                }
                print(f"Informations du conteneur {container_id} : {container_info}")
                return container_info
            else:
                print(f"Aucun conteneur trouvé avec l'ID {container_id}.")
                return None
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
    finally:
        connection.close()


# Fonction pour établir une connexion SSH avec un conteneur
def connect_ssh(container_info: tuple) -> None:
    """
    Établit une connexion SSH avec un conteneur et exécute une commande.

    Cette fonction utilise les informations fournies pour se connecter à un conteneur via SSH,
    exécute une commande simple et affiche la sortie de cette commande.

    Args:
        container_info (tuple): Un tuple contenant les informations du conteneur sous la forme
                                (nom_du_conteneur, adresse_ip, port_ssh, mot_de_passe).

    Raises:
        Exception: Si une erreur survient lors de la connexion SSH ou de l'exécution de la commande.
    """
    try:
        # Paramètres de connexion SSH
        hostname = container_info[1]  # Adresse IP ou nom d'hôte du conteneur
        port = container_info[2]  # Port SSH
        username = "client"  # Utilisateur par défaut pour la connexion SSH
        password = container_info[3]  # Mot de passe temporaire du conteneur

        # Création de l'objet SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Pour ajouter l'hôte automatiquement

        # Connexion SSH
        print(f"Connexion SSH en cours avec le conteneur {container_info[1]} sur le port {port}...")
        ssh.connect(hostname, port=port, username=username, password=password)

        # Exemple d'exécution d'une commande sur le conteneur via SSH
        stdin, stdout, stderr = ssh.exec_command('echo "Commande exécutée sur le conteneur."')
        print(stdout.read().decode())  # Affiche la sortie de la commande

        # Fermer la connexion SSH
        ssh.close()
        print(f"Connexion SSH terminée pour le conteneur {container_info[1]}.")
    except Exception as e:
        print(f"Erreur lors de la connexion SSH avec le conteneur {container_info[1]} : {e}")




























def main():
    contract_id = input("Entrez l'ID du contrat : ")
    status = check_contract_status(contract_id)
    
    if status == "active":
        print("Le contrat est activé. Vous pouvez établir une connexion SSH.")
        # Ajoutez ici le code pour établir une connexion SSH si nécessaire
        containers=get_container_info(contract_id)
    elif status in ["expired", "pending"]:
        print(f"Le contrat est dans un état non activé : {status}.")
        return
    else:
        print("Impossible de vérifier le contrat.\n contacter les administrateurs :)")
        return


    if containers:
        for container in containers:
            print(f"Traitement du conteneur : {container[1]}")
            connect_ssh(container)  # Établir la connexion SSH pour chaque conteneur actif
    else:
        print("Aucun conteneur actif trouvé.")



















if __name__ == "__main__":
    main()
