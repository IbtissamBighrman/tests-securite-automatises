# Utiliser l'image officielle Node.js comme base
FROM node:16

# Créer et définir le répertoire de travail
WORKDIR /usr/src/app

# Copier package.json et package-lock.json pour installer les dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste des fichiers du projet
COPY . .

# Exposer le port sur lequel le serveur va écouter
EXPOSE 3333

# Lancer le serveur
CMD ["tail", "-f", "/dev/null"]

