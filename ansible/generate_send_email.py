import os
import base64
import mysql.connector
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# Paramètres de connexion à la base de données MySQL
db_config = {
    'host': 'mysql-container',  # Nom du conteneur MySQL dans Docker
    'user': 'root',
    'password': 'rootpassword',  # Mot de passe root configuré
    'database': 'containers_db'  # Nom de la base de données
}

# Fonction pour générer le fichier d'informations sur le contrat
def generate_client_container_info(contract_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Récupérer les informations du contrat et du client
        cursor.execute("""
            SELECT c.client_name, c.client_email, co.contract_id, co.start_datetime, co.end_datetime, co.status
            FROM contract co
            JOIN client c ON co.client_id = c.client_id
            WHERE co.contract_id = %s
        """, (contract_id,))
        client_info = cursor.fetchone()

        if not client_info:
            print(f"Aucun contrat trouvé pour l'ID {contract_id}.")
            return None, None

        client_name, client_email, contract_id, start_datetime, end_datetime, contract_status = client_info

        # Récupérer les informations des conteneurs associés au contrat
        cursor.execute("""
            SELECT container_id, container_name, ssh_port, image, mdp_tmp
            FROM container
            WHERE contract_id = %s
        """, (contract_id,))
        containers_info = cursor.fetchall()

        # Création du fichier
        filename = f"contract_{contract_id}_containers_info.txt"
        with open(filename, "w") as f:
            f.write(f"Informations sur le client pour le contrat {contract_id} :\n")
            f.write(f"Nom du client : {client_name}\n")
            f.write(f"Email du client : {client_email}\n")
            f.write(f"Date de début du contrat : {start_datetime}\n")
            f.write(f"Date de fin du contrat : {end_datetime}\n")
            f.write(f"Statut du contrat : {contract_status}\n\n")

            if containers_info:
                f.write(f"Conteneurs associés au contrat {contract_id} :\n")
                for container in containers_info:
                    container_id, container_name, ssh_port, image, mdp_tmp = container
                    f.write(f"\nConteneur ID : {container_id}\n")
                    f.write(f"Nom du conteneur : {container_name}\n")
                    f.write(f"Port SSH : {ssh_port}\n")
                    f.write(f"Image : {image}\n")
                    f.write(f"Mot de passe temporaire : {mdp_tmp}\n")
            else:
                f.write(f"Aucun conteneur associé au contrat {contract_id}.\n")

        print(f"Fichier '{filename}' généré avec succès.")
        return filename, client_email

    except mysql.connector.Error as err:
        print(f"Erreur MySQL : {err}")
        return None, None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Fonction pour envoyer un email avec SendGrid
def send_email_with_sendgrid(subject, body, to_email, attachment_path):
    sendgrid_api_key = "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"
    message = Mail(
        from_email="clientinfos247@gmail.com",  # Adresse email de l'expéditeur
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )

    # Ajouter la pièce jointe
    if attachment_path:
        try:
            with open(attachment_path, 'rb') as f:
                data = f.read()
                encoded_file = base64.b64encode(data).decode()

            attachment = Attachment(
                FileContent(encoded_file),
                FileName(os.path.basename(attachment_path)),
                FileType('application/octet-stream'),
                Disposition('attachment')
            )
            message.attachment = attachment
        except Exception as e:
            print(f"Erreur lors de l'ajout de la pièce jointe : {e}")

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

        # Étape 1 : Générer le fichier
        attachment_path, client_email = generate_client_container_info(contract_id)

        # Étape 2 : Envoyer l'email si le fichier est généré
        if attachment_path and client_email:
            subject = "Informations sur ton contrat et conteneurs"
            body = f"""
Bonjour,

J'espère que vous allez bien.

Vous trouverez ci-joint les informations concernant votre contrat ainsi que les détails des conteneurs associés. Ce fichier inclut :
- Les informations sur votre contrat (dates, statut, etc.)
- Les détails des conteneurs associés, y compris leur nom, leur port SSH, l'image utilisée, et le mot de passe temporaire.

Veuillez trouver en pièce jointe un fichier détaillant toutes les informations.

N'hésitez pas à revenir vers nous si vous avez des questions supplémentaires.

Cordialement,

"""


            send_email_with_sendgrid(subject, body, client_email, attachment_path)
        else:
            print("Aucun email n'a été envoyé, car le fichier ou l'adresse email est manquant(e).")
    else:
        print("Veuillez entrer un identifiant de contrat valide.")
