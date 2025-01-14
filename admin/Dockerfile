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
    apache2 \
    php \
    libapache2-mod-php \
    php-mysql \
    jq \
    && apt-get clean

# Installer les modules Python nécessaires, y compris Paramiko
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade docker ansible requests mysqlclient PyMySQL mysql-connector-python sendgrid paramiko

# Installer les collections Ansible nécessaires pour Docker et MySQL
RUN ansible-galaxy collection install community.docker --force && \
    ansible-galaxy collection install community.mysql --force

# Configurer Apache pour utiliser PHP
RUN a2enmod php7.4

# Créer un répertoire pour les scripts Ansible
WORKDIR /app

# Exposer les ports nécessaires pour Docker et votre application
EXPOSE 8080 3306

# Définir la commande par défaut pour exécuter cron et apache
CMD cron && service apache2 start
