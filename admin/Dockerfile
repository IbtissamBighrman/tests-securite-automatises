# Utiliser une image de base comme Ubuntu
FROM ubuntu:20.04

# Définir l'environnement pour éviter les questions pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

# Mettre à jour et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    git \
    ansible \
    docker.io \
    cron \
    mysql-client \
    libmysqlclient-dev \
    pkg-config \
    build-essential \
    nano \  
    && apt-get clean

# Installer les modules Python nécessaires
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade docker ansible requests mysqlclient PyMySQL

# Installer les collections Ansible nécessaires pour Docker et MySQL
RUN ansible-galaxy collection install community.docker --force && \
    ansible-galaxy collection install community.mysql --force

# Créer un répertoire pour les scripts Ansible
WORKDIR /app

# Exposer les ports nécessaires pour Docker et votre application
EXPOSE 8080 3306

# Définir la commande par défaut
CMD cron -f
