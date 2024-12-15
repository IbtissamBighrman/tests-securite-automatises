# Utiliser l'image de base Ubuntu 20.04
FROM ubuntu:20.04

# Installer les outils nécessaires
RUN apt-get update && \
    apt-get install -y openssh-server sudo && \
    rm -rf /var/lib/apt/lists/*
    

# Créer les groupes 'admins' et 'clients'
RUN groupadd admins 
RUN groupadd clients

# Créer les utilisateurs 'admin1' et 'client1' et les ajouter à leurs groupes respectifs
RUN useradd -m -s /bin/bash -g admins admin1 
RUN echo 'admin1:password' | chpasswd
RUN usermod -aG sudo admin1
RUN useradd -m -s /bin/bash -g clients client1 
RUN echo 'client1:password' | chpasswd

# Appliquer des restrictions pour 'client1' : interdire la commande 'useradd' avec sudo
RUN echo "client1 ALL=(ALL) NOPASSWD: ALL, !/usr/sbin/useradd, !/usr/sbin/adduser" > /etc/sudoers.d/client1 && \
    chmod 0440 /etc/sudoers.d/client1

# Configurer SSH pour permettre l'accès uniquement aux groupes 'admins' et 'clients'
RUN mkdir /var/run/sshd && \
    echo 'root:ansible' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "AllowGroups admins clients" >> /etc/ssh/sshd_config

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le script ping_server.sh depuis le répertoire courant dans /app
COPY ping_server.sh /app/ping_server.sh

# Rendre le script exécutable
RUN chmod +x /app/ping_server.sh

# Exposer le port SSH
EXPOSE 22

# Démarrer SSH en arrière-plan
CMD ["/usr/sbin/sshd", "-D"]
