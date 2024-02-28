# Projet programmation parallèle
 
- Bathily Yahaya
- Kilimou Ambroise

## Pour lancer le projet 

> Si vous ne possédez pas l'utilitaire make veuillez copier puis coller dans l'ordre les commandes associés

### Pour les utilisateurs de windows

```
make init-env
./venv/Scripts/activate
make install-requirements
```
### Pour les utilisateurs unix

```
make init-env
source ./venv/bin/activate
make install-requirements
```

> Maintenant, vous pouvez lancer le projet en lançant la commande suivante puis en ouvrant le fichier puis en saisissant le lien suivant dans votre navigateur 

*Lien*
```
http://localhost:8080/client-interface.html
```
*Commande*

```
make launch-client
```

## Logique de fonctionnement du projet

### L'interface graphique (*communication/interface*)

> Nous avons une interface graphique qui grâce à javascript fait des requêtes vers une api afin de traiter les actions qui se passent sur la page

### L'api (*communication/client_api.py*)

> Nous avons créé une api avec fastapi, cette api sert de client au serveur et fait donc l'intermédiaire entre les requêtes de l'interface et celui ci 

### Le serveur (*communication/server.py*)

> Le serveur quand à lui joue son rôle de serveur et attend de nouvelles connexions afin de créer des instances de (*communication/server_client_manager.py*) lancés dans des threads, c'est donc ce fichier qui s'occupe de la gestion des messages entrant et de la fourniture des réponses.


### Logique des échanges sockets

> Au niveau du traitement des messages reçu (*communication.server_client_manager.py*), des actions sont définis pour savoir quelle action est attendue (récupération de la liste des ficbiers disponibles, réception des fichiers que l'utilisateur souhaite télécharger ...). A la réception donc d'une action la fonction de gestion correspondante à l'action est appellée afin de gérer ce qu'il y a à faire (réception d'autres messages ....)

> Pour transmettre un message, un premier message est toujours envoyé contenant la taille du réel message attendu, ainsi la taille exacte attendue est récupéré. Par exemple si je veux envoyer bonjour, je l'encode puis envoi sa taille en premier ainsi derrière sur mon prochain recv, je saurai quelle taille récupérer.

> Pour mettre fin à une connexion et donc libérer le thread associé le client connecté peut envoyer une action défini pour celle-ci afin que le thread arrête de tourner. 