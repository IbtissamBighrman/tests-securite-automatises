<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Créer un Contrat - Auto Pintest</title>
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
        select, input[type="datetime-local"], input[type="text"], input[type="number"] {
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

    <h2>Créer un Contrat</h2>

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

    // Requête pour récupérer la liste des clients
    $clients_sql = "SELECT client_id, client_name FROM client";
    $clients_result = $conn->query($clients_sql);

    // Requête pour récupérer la liste des targets disponibles
    $targets_sql = "SELECT target_id, network_name FROM target";
    $targets_result = $conn->query($targets_sql);

    // Requête pour récupérer les conteneurs disponibles (ceux sans contrat)
    $containers_sql = "SELECT container_id, container_name FROM container WHERE contract_id IS NULL";
    $containers_result = $conn->query($containers_sql);

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $client_id = $conn->real_escape_string($_POST['client_id']);
        $start_datetime = $conn->real_escape_string($_POST['start_datetime']);
        $end_datetime = $conn->real_escape_string($_POST['end_datetime']);
        $status = $conn->real_escape_string($_POST['status']);
        $target_id = $conn->real_escape_string($_POST['target_id']);
        $container_ids = $_POST['container_ids'];  // Récupère les conteneurs sélectionnés (un ou plusieurs)

        // Insertion du contrat
        $sql = "INSERT INTO contract (client_id, start_datetime, end_datetime, status, target_id) 
                VALUES ('$client_id', '$start_datetime', '$end_datetime', '$status', '$target_id')";
        
        if ($conn->query($sql) === TRUE) {
            // Récupération de l'ID du contrat nouvellement inséré
            $contract_id = $conn->insert_id;

            // Mise à jour des conteneurs pour les associer au contrat
            if (!empty($container_ids)) {
                foreach ($container_ids as $container_id) {
                    $update_sql = "UPDATE container SET contract_id = '$contract_id' WHERE container_id = '$container_id'";
                    $conn->query($update_sql);
                }
            }

            echo "<p style='color: green;'>Contrat ajouté avec succès et conteneurs associés !</p>";
        } else {
            echo "<p style='color: red;'>Erreur lors de l'ajout du contrat : " . $conn->error . "</p>";
        }
    }

    // Fermeture de la connexion
    $conn->close();
    ?>

    <form method="POST" action="">
        <label for="client_id">Client :</label>
        <select id="client_id" name="client_id" required>
            <?php
            if ($clients_result->num_rows > 0) {
                while ($row = $clients_result->fetch_assoc()) {
                    echo "<option value='" . $row['client_id'] . "'>" . $row['client_name'] . "</option>";
                }
            } else {
                echo "<option value=''>Aucun client trouvé</option>";
            }
            ?>
        </select>

        <label for="target_id">Cible :</label>
        <select id="target_id" name="target_id" required>
            <?php
            if ($targets_result->num_rows > 0) {
                while ($row = $targets_result->fetch_assoc()) {
                    echo "<option value='" . $row['target_id'] . "'>" . $row['network_name'] . "</option>";
                }
            } else {
                echo "<option value=''>Aucune cible trouvée</option>";
            }
            ?>
        </select>

        <label for="container_ids">Sélectionnez les conteneurs à associer :</label>
        <div>
            <?php
            if ($containers_result->num_rows > 0) {
                while ($row = $containers_result->fetch_assoc()) {
                    echo "<div>
                            <input type='checkbox' name='container_ids[]' value='" . $row['container_id'] . "' id='container_" . $row['container_id'] . "'>
                            <label for='container_" . $row['container_id'] . "'>" . $row['container_name'] . "</label>
                          </div>";
                }
            } else {
                echo "<p>Aucun conteneur disponible</p>";
            }
            ?>
        </div>

        <label for="start_datetime">Date de début :</label>
        <input type="datetime-local" id="start_datetime" name="start_datetime" required>

        <label for="end_datetime">Date de fin :</label>
        <input type="datetime-local" id="end_datetime" name="end_datetime" required>

        <label for="status">Statut :</label>
        <select id="status" name="status" required>
            <option value="active">Active</option>
            <option value="pending">En attente</option>
            <option value="expired">Expiré</option>
        </select>

        <input type="submit" value="Créer le Contrat">
    </form>

    <div class="button-container">
        <button class="btn-primary" onclick="window.location.href='index.php'">Revenir à l'Acceuil</button>
    </div>

</body>
</html>
