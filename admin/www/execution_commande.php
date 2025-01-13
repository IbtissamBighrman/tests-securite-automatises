<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exécution de Commandes Docker</title>
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
        textarea {
            width: 80%;
            height: 200px;
            margin: 20px 0;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 5px;
            background-color: #007bff;
        }
        button:hover {
            background-color: #0056b3;
        }
        pre {
            background-color: #f8f9fa;
            padding: 20px;
            margin-top: 20px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>

    <h1>Exécution de Commandes Docker</h1>

    <form method="POST" action="">
        <textarea name="docker_command" placeholder="Entrez votre commande Docker ici..."></textarea><br>
        <button type="submit">Exécuter</button>
    </form>

    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $command = escapeshellcmd($_POST['docker_command']);
        $output = shell_exec($command);
        
        if ($output) {
            echo "<pre>$output</pre>";
        } else {
            echo "<p>Erreur lors de l'exécution de la commande ou aucune sortie.</p>";
        }
    }
    ?>
    <div class="button-container">
        <button class="btn-primary" onclick="window.location.href='index.php'">Revenir à l'Acceuil</button>
    </div>
</body>
</html>
