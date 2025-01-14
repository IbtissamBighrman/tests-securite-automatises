<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Afficher les Contrats - Auto Pentest</title>
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
            margin: 20px auto;
            width: 80%;
            border-collapse: collapse;
            background-color: #f9f9f9;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:hover {
            background-color: #f1f1f1;
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
    <h1>Liste des Contrats</h1>

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

    // Vérifiez si un contrat est sélectionné
    if (isset($_GET['contract_id'])) {
        $contract_id = intval($_GET['contract_id']);

        // Requête pour récupérer les informations de la cible associée au contrat sélectionné
        $sql_target = "SELECT network_name, subnet, target_ip 
                       FROM target 
                       WHERE target_id IN (
                           SELECT target_id 
                           FROM contract 
                           WHERE contract_id = $contract_id
                       )";
        $result_target = $conn->query($sql_target);

        echo "<h2>Informations de la Cible pour le Contrat #$contract_id</h2>";

        if ($result_target->num_rows > 0) {
            echo "<table>";
            echo "<tr>
                    <th>Nom du Réseau</th>
                    <th>Sous-réseau</th>
                    <th>Adresse IP</th>
                  </tr>";
            while ($row = $result_target->fetch_assoc()) {
                echo "<tr>
                        <td>" . $row['network_name'] . "</td>
                        <td>" . $row['subnet'] . "</td>
                        <td>" . $row['target_ip'] . "</td>
                      </tr>";
            }
            echo "</table>";
        } else {
            echo "<p>Aucune cible trouvée pour ce contrat.</p>";
        }

        echo "<div class='button-container'>
                <button class='btn-primary' onclick=\"window.location.href='?'\">
                    Revenir à la liste des contrats
                </button>
              </div>";
    } elseif (isset($_GET['contract_id_containers'])) {
        $contract_id = intval($_GET['contract_id_containers']);

        // Requête pour récupérer les conteneurs liés au contrat sélectionné
        $sql_containers = "SELECT container_name, ssh_port, image 
                           FROM container 
                           WHERE contract_id = $contract_id";
        $result_containers = $conn->query($sql_containers);

        echo "<h2>Conteneurs Liés au Contrat #$contract_id</h2>";

        if ($result_containers->num_rows > 0) {
            echo "<table>";
            echo "<tr>
                    <th>Nom du Conteneur</th>
                    <th>Port SSH</th>
                    <th>Image</th>
                  </tr>";
            while ($row = $result_containers->fetch_assoc()) {
                echo "<tr>
                        <td>" . $row['container_name'] . "</td>
                        <td>" . $row['ssh_port'] . "</td>
                        <td>" . $row['image'] . "</td>
                      </tr>";
            }
            echo "</table>";
        } else {
            echo "<p>Aucun conteneur trouvé pour ce contrat.</p>";
        }

        echo "<div class='button-container'>
                <button class='btn-primary' onclick=\"window.location.href='?'\">
                    Revenir à la liste des contrats
                </button>
              </div>";
    } else {
        // Requête pour récupérer tous les contrats
        $sql_contracts = "SELECT 
                            c.contract_id, 
                            cl.client_name, 
                            c.start_datetime, 
                            c.end_datetime, 
                            c.status, 
                            t.network_name, 
                            t.target_ip 
                          FROM 
                            contract c
                          JOIN 
                            client cl ON c.client_id = cl.client_id
                          JOIN 
                            target t ON c.target_id = t.target_id";
        $result_contracts = $conn->query($sql_contracts);

        if ($result_contracts->num_rows > 0) {
            echo "<table>";
            echo "<tr>
                    <th>ID Contrat</th>
                    <th>Client</th>
                    <th>Date de Début</th>
                    <th>Date de Fin</th>
                    <th>Statut</th>
                    <th>Cible</th>
                    <th>Actions</th>
                  </tr>";
            while ($row = $result_contracts->fetch_assoc()) {
                echo "<tr>
                        <td>" . $row['contract_id'] . "</td>
                        <td>" . $row['client_name'] . "</td>
                        <td>" . $row['start_datetime'] . "</td>
                        <td>" . $row['end_datetime'] . "</td>
                        <td>" . $row['status'] . "</td>
                        <td>" . $row['network_name'] . " (" . $row['target_ip'] . ")</td>
                        <td>
                            <button class='btn-primary' onclick=\"window.location.href='?contract_id=" . $row['contract_id'] . "'\">Infos Cible</button>
                            <button class='btn-primary' onclick=\"window.location.href='?contract_id_containers=" . $row['contract_id'] . "'\">Conteneurs Liés</button>
                        </td>
                      </tr>";
            }
            echo "</table>";
        } else {
            echo "<p>Aucun contrat trouvé.</p>";
        }
    }

    // Fermeture de la connexion
    $conn->close();
    ?>

    <div class="button-container">
        <button class="btn-primary" onclick="window.location.href='index.php'">Revenir à l'Accueil</button>
    </div>
</body>
</html>
