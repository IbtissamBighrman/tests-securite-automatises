import mysql.connector
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Paramètres de connexion à la base de données MySQL
db_config = {
    'host': 'mysql-container',
    'user': 'root',
    'password': 'rootpassword',
    'database': 'containers_db'
}

# Fonction pour récupérer les informations du contrat et du client
def get_contract_info(contract_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.client_name, c.client_email, co.contract_id, co.start_datetime, co.end_datetime, co.status
            FROM contract co
            JOIN client c ON co.client_id = c.client_id
            WHERE co.contract_id = %s
        """, (contract_id,))
        client_info = cursor.fetchone()

        if not client_info:
            print(f"Aucun contrat trouvé pour l'ID {contract_id}.")
            return None, None, None, None, None, None, None

        client_name, client_email, contract_id, start_datetime, end_datetime, contract_status = client_info

        cursor.execute("""
            SELECT container_id, container_name, ssh_port, image, mdp_tmp
            FROM container
            WHERE contract_id = %s
        """, (contract_id,))
        containers_info = cursor.fetchall()

        return client_name, client_email, contract_id, start_datetime, end_datetime, contract_status, containers_info

    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return None, None, None, None, None, None, None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Fonction pour envoyer un email avec SendGrid
def send_email_with_sendgrid(subject, body, to_email):
    sendgrid_api_key = "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"
    message = Mail(
        from_email="clientinfos247@gmail.com",
        to_emails=to_email,
        subject=subject,
        html_content=body  # Format HTML ici
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        print(f"Email envoyé avec succès à {to_email} ! Statut : {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {e}")

# Fonction principale
if __name__ == "__main__":
    contract_id_input = input("Entrez l'ID du contrat : ")
    if contract_id_input.isdigit():
        contract_id = int(contract_id_input)

        client_name, client_email, contract_id, start_datetime, end_datetime, contract_status, containers_info = get_contract_info(contract_id)

        if client_email:
            subject = "📄 Informations sur votre contrat et vos conteneurs"
            
            # Construire le corps HTML de l'email
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #4CAF50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f4f4f4;
            color: #333;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <h1>Informations sur votre contrat</h1>
    <p>Bonjour <strong>{client_name}</strong>,</p>
    <p>Voici les détails de votre contrat :</p>
    <ul>
        <li><strong>ID du contrat :</strong> {contract_id}</li>
        <li><strong>Date de début :</strong> {start_datetime}</li>
        <li><strong>Date de fin :</strong> {end_datetime}</li>
        <li><strong>Statut :</strong> {contract_status}</li>
    </ul>
    <h2>Conteneurs associés</h2>
"""

            if containers_info:
                body += """
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nom</th>
                <th>Port SSH</th>
                <th>Image</th>
                <th>Mot de passe temporaire</th>
            </tr>
        </thead>
        <tbody>
"""
                for container_id, container_name, ssh_port, image, mdp_tmp in containers_info:
                    body += f"""
            <tr>
                <td>{container_id}</td>
                <td>{container_name}</td>
                <td>{ssh_port}</td>
                <td>{image}</td>
                <td>{mdp_tmp}</td>
            </tr>
"""
                body += """
        </tbody>
    </table>
"""
            else:
                body += "<p>Aucun conteneur n'est associé à ce contrat.</p>"

            body += """
    <p>Pour toute question, n'hésitez pas à nous contacter.</p>
    <p>Cordialement,<br>L'équipe technique</p>
</body>
</html>
"""

            send_email_with_sendgrid(subject, body, client_email)
        else:
            print("Erreur : Impossible de trouver l'adresse email du client pour cet ID de contrat.")
    else:
        print("Veuillez entrer un identifiant de contrat valide.")
