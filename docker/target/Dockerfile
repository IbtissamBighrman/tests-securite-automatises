# docker/target/Dockerfile
FROM node:14

# Créer le répertoire de l'application
WORKDIR /usr/src/app

# Copier l'application
COPY app.js .

# Exposer le port de l'application
EXPOSE 3000

# Démarrer le serveur Node.js
CMD ["node", "app.js"]
