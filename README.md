# 🛠️ **Automated "Pentest" Project**

---

## 📋 **Table des Matières**

- [📜 Contexte](#📜-contexte)
- [🔑 Prérequis](#🔑-prérequis)
- [⚙️ Installation et Exécution](#⚙️-installation-et-exécution)
- [🌐 Architecture](#🌐-architecture)
- [📌 Informations utiles](#📌-informations-utiles)

---

## 📜 **Contexte**

> 🕵️‍♂️ I'm living in an **RGPD-free country** where laws are cool concerning privacy and the fact you may "borrow" computing resources.  
I also have software that turns any containers I do "control" into a **node helping my clients** to do some **"pentests"**:  
➡️ **DDoS**,  
➡️ **Phishing**,  
... to name a few.

🔄 **Problem**:  
- I experience issues with losing containers from time to time.  
- Luckily, I also gain control of new resources periodically.  

🔧 **Objective**:  
To create a tool that ensures **quality of service** by maintaining a (relatively) constant number of resources for my clients from my resource pool.

---

## 🔑 **Prérequis**

- 🐳 [Docker](https://docs.docker.com/get-docker/) (version 20.10 ou supérieure)
- ⚙️ [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_install.html) (version 2.9 ou supérieure)
- 🖥️ Accès à un terminal Linux (**Kali Linux recommandé**)

---

## ⚙️ **Installation et Exécution**

1. **📂 Cloner le dépôt :**
   ```bash
   git clone https://github.com/IbtissamBighrman/tests-securite-automatises.git
   ```

2. **📂 Dans le répertoire 'admin', exécutez la commande suivante :**
   ```bash
   docker-compose up
   ```

3. **🔗 Accédez au conteneur 'admin-container' :**
   ```bash
   docker exec -it admin-container /bin/bash
   ```

4. **📦 Dans le répertoire 'ansible', exécutez la commande suivante :**
   - *Cette commande permet de générer un nombre **N** de conteneurs.*
   ```bash
   ansible-playbook -i inventory playbook.yml
   ```

5. **🎯 Créer un conteneur cible et l'associer à un réseau :**
   - *Dans le répertoire 'cible' :*
   ```bash
   ansible-playbook -i inventory playbook.yml
   ```
   - *Cela crée un `container_target<id_cible>` et un `network_target<id_cible>`.*

6. **🚀 Lancer le serveur Apache pour accéder à l'interface graphique :**
   ```bash
   service apache2 start
   ```
   - 🔗 *L'interface admin est accessible ici : [http://localhost:8081](http://localhost:8081).*

7. **📜 Dans le répertoire 'ansible', exécutez le script suivant :**
   ```bash
   ./nouveau_contrat.sh <id_contract>
   ```
   - Ce script permet de :
     - 🔗 Connecter les conteneurs attaquants au réseau de la cible.
     - ✉️ Envoyer un email de confirmation au client (avec identifiants SSH).
     - 📤 Transférer un script d'attaque vers les conteneurs attaquants et lancer l'attaque (*optionnel* : le client peut créer son propre script).

---

## 🌐 **Architecture**

![architecture](./img/shema_architecture.png)

---

## 📌 **Informations utiles**

### 🗄️ **Base de Données (BDD)**

![bdd](./img/bdd.png)

1. **Pour accéder à la BDD :**
   ```bash
   docker exec -it mysql-container mysql -u root -p
   ```

2. **Mot de passe :**
   ```bash
   rootpassword
   ```

3. **Commandes utiles :**
   ```bash
   USE containers_db;
   ```

   ```bash
   SHOW TABLES;
   ```

---

### 🕒 **Tâches planifiées**

- 🔍 **verifier_contrats_expires.sh**  
- 🛠️ **conteneur_endommages.sh**

---

> 📝 **Note** : Ce projet est destiné à un usage contrôlé et responsable uniquement. Soyez toujours conscients des lois et de l'éthique dans vos projets.
