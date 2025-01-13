<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Créer un Client - Auto Pintest</title>
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
        form {
            margin: 20px auto;
            width: 50%;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"], input[type="email"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .button-container {
            margin-top: 20px;
        }
        .button-container button {
            padding: 10px 20px;
            font-size: 16px;
            margin: 5px;
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
    </style>
</head>
<body>

    <h1>Auto Pintest</h1>

    <h2>Créer un Client</h2>

    <?php
    // Informations de connexion à la base de données
    $host = 'mysql-container';
    $user = 'root';
    $password = 'rootpassword';
    $dbname = 'containers_db';

    // Connexion à MySQL
    $conn = new mysqli($host, $user, $password, $dbname);

    // Vérifiez la connexion
    if ($conn->connect_error) {
        die("Échec de la connexion : " . $conn->connect_error);
    }

    // Traiter le formulaire de création de client
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $client_name = $conn->real_escape_string($_POST['client_name']);
        $client_email = $conn->real_escape_string($_POST['client_email']);

        $sql = "INSERT INTO client (client_name, client_email) VALUES ('$client_name', '$client_email')";

        if ($conn->query($sql) === TRUE) {
            echo "<p style='color: green;'>Client ajouté avec succès !</p>";
        } else {
            echo "<p style='color: red;'>Erreur lors de l'ajout du client : " . $conn->error . "</p>";
        }
    }

    // Fermeture de la connexion
    $conn->close();
    ?>

    <form method="POST" action="">
        <label for="client_name">Nom du Client :</label>
        <input type="text" id="client_name" name="client_name" required>

        <label for="client_email">Email du Client :</label>
        <input type="email" id="client_email" name="client_email" required>

        <input type="submit" value="Ajouter le Client">
    </form>

    <div class="button-container">
        <button class="btn-primary" onclick="window.location.href='index.php'">Revenir à l'Acceuil</button>
    </div>

</body>
</html>
