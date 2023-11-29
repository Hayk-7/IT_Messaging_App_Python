"""
Créé le 4/10/23 à 13:00

@author: H, R
"""

import client
import interface

def main():
    """
    Fonction principale pour exécuter le programme.
    """
    try:
        # Demander à l'utilisateur les informations de connexion
        login = input("Entrez votre identifiant : ")

        # Créer un client en utilisant l'identifiant fourni
        localClient = client.Client(login)

        # Connecter le client au serveur
        localClient.connect()

        # Créer la fenêtre principale avec des dimensions spécifiées et le
        # client connecté
        main_window = interface.WhatsDownMainWindow(480, 700, localClient)

    except Exception as e:
        # Gérer les exceptions et afficher un message d'erreur
        print(f"[EXCEPTION] Une erreur s'est produite : {e}")
        quit()

if __name__ == '__main__':
    # Exécuter la fonction principale si le script est exécuté en tant que
    # module principal
    main()
