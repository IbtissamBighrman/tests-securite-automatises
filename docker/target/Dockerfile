# Dockerfile pour le conteneur cible
FROM ubuntu:20.04

# Installer les outils nécessaires
RUN apt-get update && \
    apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*

# Garder le conteneur en vie
CMD ["tail", "-f", "/dev/null"]
