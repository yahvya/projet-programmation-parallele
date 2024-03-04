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
- **Makefile** : (*fichier contenant les commandes utiles pour le lancement du projet*)

## Fonctionnement du projet

> L'IHM communique avec l'api. L'api représente donc un client du serveur avec lequel il communique via l'utilitaire de transmission via des messages au format (taille|message). Le serveur à la réception d'une connexion crée un gestionnaire client qui se charge de fournir les résultats des actions reçues.

> Au niveau de la compression l'arbre est représentée par un format json left right puis une fois les binaires associés, transformé en json {caractère : binaire}

> Pour le traitement global, à chaque étape de la compression une fonction callback associé à l'étape est appellé permettant de fonctionner par stream (ex : une fois l'arbre crée l'arbre est envoyé dans sa version compressée)

> Pour vérifier que la compression se fait bien, veuillez ajouter le code suivant dans *huffman_compression/huffman_compressor.py*, en lançant ce même fichier, vous aurez dans le dossier *ressources* un fichier resultat_compression.txt dont vous pourrez comparer la taille avec *ressources/fichier-1.txt* qui est le fichier compressé

```
with open("../ressources/resultat-compression.txt", "wb+") as f:
    f.write(huffman_compressor.create_compression_stream(
        filepath="../ressources/fichier-1.txt",
        to_do_on_compression_error=lambda error: print(error.get_error_message())
    ).read())
```

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