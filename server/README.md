## Dossier serveur

Ce dossier contient le code source du serveur. 
Pour avoir un environnement fonctionnel, suivre la procédure suivante :

1. Installer l'interpreteur python version 3.6 ou plus
2. Lancer l'invite de commande et se positionner dans le dossier server
3. Créer un environnement virtual venv et l'activer
4. Exécuter la commande : 'pip3 install -r requirements.txt' pour installer les paquets nécessaires.
5. Exécuter la commande : 'python3 main.py default' pour initialiser la bd avec des données importantes par défaut.

Une fois l'environnement complètement installée, vous pouvez :

* Lancer le serveur avec : python3 main.py runserver    (bien vouloir se rassurer que le port 4700 est libre)
* Lancer la recherche de nouveaux sites phishing référencés avec : python3 main.py search


## Dossier addons

Ce dossier contient le code source de l'addons instalable sur un browser :

- Chromium : addons qui fonctionne sur les navigateurs Chrome et Opera
- Firefox : addons qui fonctionne le navigateur Firefox

Pour installer un addons en local, se rendre dans les paramètres du navigateur, option 'Extensions'.
