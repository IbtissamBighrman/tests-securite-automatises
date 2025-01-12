-- Création de la base de données
CREATE DATABASE IF NOT EXISTS containers_db;

-- Utilisation de la base de données nouvellement créée
USE containers_db;

-- Table clients : Contient les informations des clients
CREATE TABLE IF NOT EXISTS client (
    client_id INT AUTO_INCREMENT PRIMARY KEY,   -- Identifiant unique pour chaque client
    client_name VARCHAR(255) NOT NULL,          -- Nom du client
    client_email VARCHAR(255) NOT NULL UNIQUE   -- Email unique du client
);

-- Table contrats : Contient les informations des contrats liés à un client
CREATE TABLE IF NOT EXISTS contract (
    contract_id INT AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque contrat
    client_id INT NOT NULL,                      -- Lien avec la table clients
    start_datetime DATETIME NOT NULL,            -- Date et heure de début du contrat
    end_datetime DATETIME NOT NULL,              -- Date et heure de fin du contrat
    status ENUM('active', 'expired', 'pending') NOT NULL,  -- Statut du contrat (active, expired, pending)
    FOREIGN KEY (client_id) REFERENCES client(client_id) ON DELETE CASCADE  -- Clé étrangère avec la table client
);

-- Table containers : Contient les informations des conteneurs liés à un contrat
CREATE TABLE IF NOT EXISTS container (
    container_id VARCHAR(255) PRIMARY KEY,              -- Identifiant unique du conteneur, pas auto-incrémenté
    contract_id INT DEFAULT NULL,                       -- Lien avec la table contrats (peut être NULL)
    container_name VARCHAR(255) NOT NULL,              -- Nom du conteneur
    ssh_port INT,                                       -- Port SSH pour se connecter au conteneur
    image VARCHAR(255) NOT NULL,                       -- Image utilisée pour créer le conteneur
    mdp_tmp VARCHAR(255) NOT NULL,                     -- Mot de passe temporaire pour client1
    CONSTRAINT fk_contract FOREIGN KEY (contract_id) 
        REFERENCES contract(contract_id) 
        ON DELETE SET NULL,                            -- Clé étrangère avec la table contract
    INDEX idx_container_type (container_name)          -- Index pour différencier admin et client (si un préfixe ou pattern est utilisé)
);


-- Table targets : Contient les informations des cibles réseau liées à un contrat
CREATE TABLE IF NOT EXISTS target (
    target_id INT AUTO_INCREMENT PRIMARY KEY,  -- Identifiant unique pour chaque cible
    contract_id INT NOT NULL,                  -- Lien avec la table contrats
    target_network VARCHAR(18) NOT NULL,       -- Réseau cible au format CIDR (exemple: 192.168.1.0/24)
    target_ip VARCHAR(15) NOT NULL,            -- Adresse IP cible
    FOREIGN KEY (contract_id) 
        REFERENCES contract(contract_id) 
        ON DELETE CASCADE                      -- Clé étrangère avec la table contract
);



-- Insertion de quelques clients
INSERT INTO client (client_name, client_email) VALUES
('Client A', 'clientA@example.com'),
('Client B', 'clientB@example.com'),
('Client C', 'clientC@example.com');

-- Insertion de quelques contrats
INSERT INTO contract (client_id, start_datetime, end_datetime, status) VALUES
(1, '2024-01-01 08:00:00', '2024-01-24 18:20:00', 'active'),
(2, '2024-02-01 09:00:00', '2024-12-31 18:00:00', 'pending'),
(3, '2024-03-01 10:00:00', '2024-12-31 18:00:00', 'expired');
