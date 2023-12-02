# IT_Messaging_App_Python
# Chat Python - Client et Serveur

## Introduction
Ceci est notre projet de semestrielle qui permet d'envoyer des messages entre différents appareils sur un même réseau.
Il est composé de 4 fichiers Python: main.py, interface.py, client.py et server.py.

## Main.py

Le fichier `main.py` est le système de contrôle. C'est le code que chaque personne doit avoir pour utiliser le chat.
Tout d'abord, il demande le login et ensuite, il ouvre la fenêtre du chat.

## Interface.py

Ce ficher traite l'affichage de la fenêtre

## Client.py

Le fichier `client.py` contient le code pour le client du chat.

## Server.py

Le fichier `server.py` contient le code pour le serveur du chat.


## Utilisation

Il y a 4 choses à configurer avant de pouvoir utiliser le code correctement:

- Installer les modules non présent sur l'ordinateur
- Lancer le serveur
- Corriger l'addresse IP
- Lancer le code 

1. **Installation des fichiers de base** : 
  Dans notre projet, beaucoup de modules sont utilisés: os, sys, tkinter, PIL (pillow), datetime, time, math, socket et threading.
  La plupart sont installés par défaut, mais PIL ne l'est pas. Pour l'avoir, dans un terminal, écrivez:
  `pip install pillow`

Vous avez maintenant toutes les ressources nécessaires.

2. **Activation du server**:
   Avant de démarrer l'interface, il faut activer le serveur. Sinon, on ne pourra pas communiquer les messages d'un ordinateur à un autre.
  **ATTENTION: POUR UTILISER CETTE APP, LES UTILISATEURS DOIVENT TOUS ÊTRE SUR LE MÊME RÉSEAU.**
   Pour démarrer le serveur, ouvrez simplement le fichier `server.py` et faites tourner le code **sur un seul des ordinateurs du résaux**

3. **Correction de l'addresse IP**:

4. **Vous êtes prêt**:
   Ouvrez le code `main.py` et tournez le code.
   Enjoy your chat with whatsdown.


## Commandes spéciales:

Si vous commencez le message avec /, le code interpretera cela comme une commande spéciale.

1. `/fibonacci {int}`: comme son nom l'indique, cette commande affiche les {int}eme nombre de la suite de Fibonacci.
