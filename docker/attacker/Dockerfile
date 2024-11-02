# Dockerfile pour le conteneur serveur qui envoie des pings
FROM ubuntu:20.04

# Installer les outils nécessaires
RUN apt-get update && \
    apt-get install -y iputils-ping bash && \
    rm -rf /var/lib/apt/lists/*

# Copier le script de ping dans le conteneur
COPY ping_server.sh /usr/local/bin/ping_server.sh

# Rendre le script exécutable
RUN chmod +x /usr/local/bin/ping_server.sh

# Commande pour exécuter le script
CMD ["/usr/local/bin/ping_server.sh"]
