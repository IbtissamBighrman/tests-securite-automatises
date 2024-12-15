import secrets
import string

# Définir les caractères possibles pour le mot de passe
alphabet = string.ascii_letters + string.digits + string.punctuation

# Générer un mot de passe aléatoire de 16 caractères
password = ''.join(secrets.choice(alphabet) for i in range(16))

print(password)
