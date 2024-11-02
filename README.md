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
2. **Dans le répertoire 'ansible' executez la commande suivante :**
  ```bash
  ansible-playbook -i inventory playbook.yml

