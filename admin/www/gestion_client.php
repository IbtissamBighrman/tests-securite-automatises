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

// Requête pour vérifier les données
$sql = "SELECT * FROM client"; 
$result = $conn->query($sql);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestion des Clients - Auto Pintest</title>
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
        table {
            width: 80%;
            margin: 20px auto;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border: 1px solid #007bff;
            text-align: left;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
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

    <h2>Gestion des Clients</h2>

    <?php
    if ($result->num_rows > 0) {
        echo "<table>";
        echo "<tr><th>ID</th><th>Nom</th><th>Email</th></tr>";
        while ($row = $result->fetch_assoc()) {
            echo "<tr><td>" . $row["client_id"] . "</td><td>" . $row["client_name"] . "</td><td>" . $row["client_email"] . "</td></tr>";
        }
        echo "</table>";
    } else {
        echo "Aucun résultat trouvé.";
    }

    // Fermer la connexion
    $conn->close();
    ?>

    <div class="button-container">
        <button class="btn-primary" onclick="window.location.href='index.php'">Revenir à l'Acceuil</button>
    </div>

</body>
</html>
