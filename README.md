## Table des Matières

- [Contexte](#contexte)
- [Prérequis](#prérequis)
- [Installation et Exécution](#installation-et-exécution)



## Contexte 

Automatisé "Pentest"

  Je vis dans un pays sans RGPD où les lois sont cool concernant la vie privée, et le fait que vous pouvez "emprunter" des ressources informatiques. J'ai également un logiciel qui transforme tous les contaners que je fais "contrôle" en un nœud aidant mes clients à faire un "pentest": DDoS, phishing pour n'en nommer que quelques-uns. Mes clients aiment me demander certains de ces conteneurs que je "contrôle" afin de faire un "pentest" sur leur infrastructure "amis". 

Je rencontre de temps en temps des problèmes avec les conteneurs que je contrôle, et je les perds. Heureusement, il arrive que je prenne également le contrôle de nouvelles ressources de temps en temps. Je veux avoir un outil me permettant d'offrir une certaine qualité de serrvice à mon client, en leur fournissant, hors de mon pool de ressources, un nombre (assez) constant de ressources. 

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 ou supérieure)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_install.html) (version 2.9 ou supérieure)
- Accès à un terminal Linux (Kali Linux recommandé)



## Installation et Exécution 

1. **Cloner le dépôt :**
  ```bash
    git clone https://github.com/IbtissamBighrman/tests-securite-automatises.git
  ```
2. **Dans le répertoire 'admin' executez la commande suivante :**
  ```bash
    docker-compose up
  ```
3. **Accedez au conteneur 'admin-container' :**
  ```bash
    docker exec -it admin-container /bin/bash
  ```
4. **Dans le repertoire 'ansible' executez la commande suivante :**
   - *grâce à cette commande vous pouvez générer un nombre N de conteneurs*
  ```bash
    ansible-playbook -i inventory playbook.yml
  ```

## Informations utiles ##
1. **BDD :**
   
  1.1.1 *Pour acceder à la BDD:*
  ```bash
    docker exec -it mysql-container mysql -u root -p
  ```
  1.1.2 *mdp:*
  ```bash
    rootpassword
  ```
  1.2 *Commandes utiles:*
  ```bash
    USE containers_db;
  ```

  ```bash
    SHOW TABLES;
  ```
2. **Les Tâches planifiées**
   - verifier_contrats_expires.sh

## To do :
`oussama + othman:`
  - Amélioration de la base de données
    ->db_init.sql (fichier à modifier)
  - shématiser la base
  - Il faut au début avoir qu'un seul sous réseau parce que on sait pas la machine cible, des qu'on sait @ip de la cible on créer le 2eme sous réseau, 
      -> ansible playbook.yml (fichier à modifier)
    
`Aymen :`
- Interface pour la administration (ajouter un client, création des contrat, augmenter le nbr de conteneurs, ….)
    
    + v0: interface terminal ;

    + v2 interface graphique

- choisissez :
  
  - Amélioration "supprimer_conteneurs_endommages.sh":
    
    ○ Vérifier si le conteneur endommagé est affecté à un client :
    
    +  Verifier si on un conteneur disonnible :
        
          si oui remplacer le conteneur, Sinon création de nouveau conteneur + remplacement
    +  Informer le client et lui envoyer les identifient pour se connecter en ssh
  
  - Script d'Attack plus une simulation pour le test 
  - (amélioration) si le client demande 1000 ressources il a besoin de se connectée 10000 c'est chiant (une autre solution)

  - Mail pour le client si le contrat Dead 
      -> verifier_contrats_expires.sh (fichier à modifier)
  - Envoyer les données de connexion ssh par mail (mot de passe temp)


  - rapport+présentation (htal mn be3d)

  
