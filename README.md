# IT_Messaging_App_Python
# Chat Python - Client et Serveur

## Introduction
Dans ce projet, nous allons créer un simple chat en utilisant Python. Le chat sera composé de deux parties : le client et le serveur. Le client permettra aux utilisateurs de se connecter et d'envoyer des messages au serveur, qui redistribuera ces messages à tous les clients connectés.

## Client.py

Le fichier `client.py` contient le code pour le client du chat.

1. **Importation du module `socket`** : Nous importons le module `socket` qui nous permet de gérer la communication réseau.

2. **Paramètres du serveur** : Nous définissons les paramètres du serveur, tels que l'adresse IP (`SERVER_IP`) et le port (`SERVER_PORT`) auxquels le client se connectera.

3. **Création du socket client** : Nous créons un socket client avec `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`. Cela crée un socket TCP/IP pour la communication.

4. **Connexion au serveur** : Nous nous connectons au serveur en utilisant `client_socket.connect((SERVER_IP, SERVER_PORT))`.

5. **Boucle d'envoi de messages** : Une boucle infinie permet à l'utilisateur d'entrer des messages à envoyer au serveur. Les messages sont lus depuis la console avec `input()`.

6. **Envoi de messages** : Les messages saisis par l'utilisateur sont envoyés au serveur à l'aide de `client_socket.send(message.encode())`. Le message est encodé en bytes avant d'être envoyé.

7. **Fermeture du socket** : Lorsque l'utilisateur quitte le chat, le socket client est fermé.

## Server.py

Le fichier `server.py` contient le code pour le serveur du chat.

1. **Importation des modules `socket` et `threading`** : Nous importons le module `socket` pour la communication réseau et le module `threading` pour gérer plusieurs connexions clientes en parallèle.

2. **Paramètres du serveur** : Nous définissons les paramètres du serveur, tels que l'adresse IP (`SERVER_IP`) et le port (`SERVER_PORT`) auxquels le serveur écoute les connexions clientes.

3. **Création du socket serveur** : Nous créons un socket serveur avec `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`. Cela crée un socket TCP/IP pour la communication avec les clients.

4. **Liaison du socket serveur** : Nous lions le socket serveur à l'adresse IP et au port spécifiés avec `server_socket.bind((SERVER_IP, SERVER_PORT))`.

5. **Mise en écoute des connexions entrantes** : Le serveur se met en écoute des connexions entrantes avec `server_socket.listen()`.

6. **Liste des clients** : Nous créons une liste `clients` pour suivre les clients connectés.

7. **Fonction de gestion des clients** : Nous définissons une fonction `handle_client(client_socket)` qui gère la communication avec chaque client connecté. Elle reçoit les messages des clients et les renvoie à tous les autres clients connectés.

8. **Boucle principale** : Dans la boucle principale, le serveur accepte les connexions entrantes avec `server_socket.accept()`. Lorsqu'un client se connecte, son socket est ajouté à la liste `clients`, et un thread est créé pour gérer ce client avec la fonction `handle_client`.

En résumé, le client.py permet à un utilisateur d'envoyer des messages au serveur, tandis que le server.py gère les connexions clientes, reçoit les messages des clients et les redistribue à tous les clients connectés. Le serveur peut gérer plusieurs clients en même temps grâce à l'utilisation de threads. Ce code forme la base d'un chat simple en Python, que vous pouvez développer davantage pour ajouter des fonctionnalités et améliorer la convivialité.
