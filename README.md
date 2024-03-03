# Projet de programmation parallèle (M1)

> Projet visant à simuler la transmission de fichiers par réseau en utilisant l'algorithme de compression huffman

## Groupe

- BATHILY YAHAYA
- KILIMOU AMBROISE

## Structure du projet

- **communication** :
  - client.py (*class de gestion d'un client du serveur*)
  - server.py (*class de gestion du serveur fournisseur de fichiers*)
  - transmission_manager.py (*class de gestion de transmission de messages réseau*)
- **huffman_compression** :
  - huffman_compressor.py (*class de gestion de compression d'un fichier*)
  - huffman_decompressor.py (*class de gestion de décompression d'un fichier*)
- **interface** :
  - api.py (*class de gestion de l'api de liaison interface serveur*)
  - visual (*dossier contenant les élements de l'IHM*)
- **ressources** : (*dossier contenant les fichiers proposés au téléchargement par le serveur*)
- **app.py** : (*fichier de lancement des différents programmes de l'application*)
- **Makefile** : (*fichier contenant les commandes utiles pour le lancement du projet*)

## Fonctionnement du projet

> L'IHM communique avec l'api. L'api représente donc un client du serveur avec lequel il communique via l'utilitaire de transmission via des messages au format (taille|message). Le serveur à la réception d'une connexion crée un gestionnaire client qui se charge de fournir les résultats des actions reçues.

> Au niveau de la compression l'arbre est représentée par un format json left right puis une fois les binaires associés, transformé en json {caractère : binaire}

> Pour le traitement global, à chaque étape de la compression une fonction callback associé à l'étape est appellé permettant de fonctionner par stream (ex: une fois l'arbre crée l'arbre est envoyé dans sa version compressée) 

## Lancement du projet

> Comme spécifié l'utilitaire make est utilisé afin de faciliter les actions, toutefois si vous ne le possédez pas, copiez coller les commandes associées directement dans le terminal suffira.

- Initialisez l'application en exécutant

```
make init-app
```

- Lancez ensuite l'environnement python 
  - Sur windows
    ```
    venv/Scripts/activate
    ```
  - Sur unix
    ```
    source venv/bin/activate || ./venv/bin/activate
    ```

- Installez les librairies utilisées puis lancez l'application

```
make install-requirements launch-app
```

- Rendez-vous ensuite dans votre navigateur sur le lien suivant
```
http://localhost:8080/app.html
```