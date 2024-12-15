# Utiliser une image de base avec Python installé
FROM python:3.9-slim

# Créer un répertoire pour l'application
WORKDIR /app

# Exposer le port sur lequel le serveur écoute
EXPOSE 8080

# Lancer le serveur HTTP
CMD ["python3", "-m", "http.server", "8080"]
