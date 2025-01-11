// Importer Express
const express = require('express');
const app = express();
const port = 3000;

// Définir une route simple
app.get('/', (req, res) => {
  res.send('Hello World!');
});

// Démarrer le serveur
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
