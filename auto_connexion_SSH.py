#################################################
#pour vérifier que les connexion ssh ok         #
#   sudo apt install net-tools                  #
#   netstat -tuln | grep :<port>                #
#       exemple: netstat -tuln | grep :22*      #
#                                               #   
#################################################


#don't forget to install pymysql and paramiko
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



def get_containers_by_contract(contract_id):
    """
    Récupère tous les conteneurs associés à un contrat spécifique.

    Args:
        contract_id (int): L'ID du contrat pour lequel récupérer les conteneurs.

    Returns:
        list: Une liste de dictionnaires contenant les informations des conteneurs associés au contrat.
              Chaque dictionnaire a les clés suivantes : 'container_id', 'container_name', 'ssh_port', 'image', 'mdp_tmp'.
              Retourne None si aucun conteneur n'est trouvé ou en cas d'erreur de connexion.
    """
    # Connexion à la base de données
    connection = connect_to_db()
    if not connection:
        return None
    
    try:
        with connection.cursor() as cursor:
            # Requête pour récupérer les conteneurs liés à un contrat
            sql_query = """
            SELECT c.container_id, c.container_name, c.ssh_port, c.image, c.mdp_tmp
            FROM container c
            WHERE c.contract_id = %s;
            """
            cursor.execute(sql_query, (contract_id,))
            results = cursor.fetchall()

            if results:
                containers = []
                # Parcours des résultats et création de la liste des conteneurs
                for result in results:
                    containers.append({
                        'container_id': result[0],
                        'container_name': result[1],
                        'ssh_port': result[2],
                        'image': result[3],
                        'mdp_tmp': result[4]
                    })
                print(f"Conteneurs liés au contrat {contract_id} : {containers}")
                return containers
            else:
                print(f"Aucun conteneur trouvé pour le contrat {contract_id}.")
                return None
    except pymysql.MySQLError as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return None
    finally:
        # Fermeture de la connexion à la base de données
        connection.close()





def connect_ssh(container_info: dict) -> None:
    """
    Établit une connexion SSH avec un conteneur et exécute une commande.

    Args:
        container_info (dict): Dictionnaire contenant les informations du conteneur sous la forme :
                               {
                                   'container_id': int,
                                   'container_name': str,
                                   'ssh_port': int,
                                   'image': str,
                                   'mdp_tmp': str
                               }

    Raises:
        Exception: Si une erreur survient lors de la connexion SSH ou de l'exécution de la commande.
    """
    # Vérification des paramètres
    required_keys = ['container_id', 'container_name', 'ssh_port', 'mdp_tmp']
    if not all(key in container_info for key in required_keys):
        print("Erreur : Les informations du conteneur sont incomplètes.")
        return

    try:
        # Paramètres de connexion SSH
        hostname = "127.0.0.1"  # Adresse IP (assume localhost pour ce cas)
        port = container_info['ssh_port']  # Port SSH
        username = "client1"  # Nom d'utilisateur par défaut
        password = container_info['mdp_tmp']  # Mot de passe temporaire du conteneur

        # Création de l'objet SSHClient
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Accepte automatiquement les clés non reconnues

        # Connexion SSH
        print(f"Connexion SSH en cours avec le conteneur {container_info['container_name']} sur le port {port}...")
        ssh.connect(hostname, port=port, username=username, password=password)

        # Exemple d'exécution d'une commande sur le conteneur via SSH
        command = 'echo "Connexion établie avec succès !"'
        stdin, stdout, stderr = ssh.exec_command(command)

        # Affichage des résultats de la commande
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if output:
            print(f"Sortie de la commande : {output}")
        if error:
            print(f"Erreur de la commande : {error}")

        # Fermeture de la connexion SSH
        ssh.close()
        print(f"Connexion SSH terminée pour le conteneur {container_info['container_name']}.")
    except paramiko.AuthenticationException:
        print(f"Erreur d'authentification pour le conteneur {container_info['container_name']}. Vérifiez les identifiants.")
    except paramiko.SSHException as ssh_error:
        print(f"Erreur SSH avec le conteneur {container_info['container_name']} : {ssh_error}")
    except Exception as e:
        print(f"Erreur imprévue lors de la connexion SSH avec le conteneur {container_info['container_name']} : {e}")




def main():
    """
    Fonction principale qui vérifie le statut d'un contrat et établit des connexions SSH 
    aux conteneurs associés si le contrat est actif.
    """
    try:
        contract_id = int(input("Entrez l'ID du contrat : "))  # Conversion en entier
    except ValueError:
        print("Erreur : L'ID du contrat doit être un nombre entier.")
        return

    # Vérification du statut du contrat
    status = check_contract_status(contract_id)
    
    if status == "active":
        print("Le contrat est activé. Récupération des informations des conteneurs...")
        containers = get_containers_by_contract(contract_id)  
        
        if containers:
            for container in containers:
                print(f"Traitement du conteneur : {container['container_name']}")
                connect_ssh(container)  # Établir la connexion SSH pour chaque conteneur actif
        else:
            print(f"Aucun conteneur actif trouvé pour le contrat {contract_id}.")
    elif status in ["expired", "pending"]:
        print(f"Le contrat est dans un état non activé : {status}.")
    else:
        print("Impossible de vérifier le contrat. Veuillez contacter les administrateurs.")




















if __name__ == "__main__":
    main()
