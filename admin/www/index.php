<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestion des Clients et Contrats</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            text-align: center;
        }
        h1 {
            margin-top: 50px;
            color: white;
            background-color: #007bff;
            padding: 20px 0;
            border-radius: 5px;
        }
        .button-container {
            margin-top: 30px;
        }
        .button-container button {
            padding: 15px 30px;
            font-size: 16px;
            margin: 10px;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 5px;
        }
        .button-container button:hover {
            background-color: #0056b3;
        }
        .button-container .btn-primary {
            background-color: #007bff;
        }
        .button-container .btn-success {
            background-color: #28a745;
        }
        .button-container .btn-warning {
            background-color: #ffc107;
        }
        .button-container .btn-danger {
            background-color: #dc3545;
        }
    </style>
</head>
<body>

    <h1>Auto Pentest</h1>

    <div class="button-container">
        <button class="btn-primary" onclick="window.location.href='gestion_client.php'">Afficher tous les clients</button>
        <button class="btn-success" onclick="window.location.href='creation_client.php'">Créer un client</button>
        <button class="btn-warning" onclick="window.location.href='creation_contrat.php'">Créer un contrat</button>
        <button class="btn-danger" onclick="window.location.href='afficher_contrats.php'">Afficher tous les contrats</button>
        <button class="btn-warning" onclick="window.location.href='desactiver_contrat.php'">Désactiver un contrat</button>
        

    </div>

</body>
</html>
