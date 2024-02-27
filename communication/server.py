import socket
from communication_exception import communication_exception
from communication_config import communication_config
from server_client_manager import server_client_manager


##
# @brief class de gestion du serveur du projet
class server:
    server = None

    ##
    # @brief configure le lancement du serveur
    # @throws communication_exception en cas d'erreur
    @staticmethod
    def launch_server():
        try:
            # création du serveur
            server.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # configuration du serveur
            server.server.bind((communication_config.address, communication_config.port))
        except Exception as _:
            raise communication_exception("Echec de lancement du serveur")

    ##
    # @brief configure l'acception des clients
    # @throws communication_exception en cas d'erreur
    @staticmethod
    def accept_clients():
        if server.server is None:
            raise communication_exception("La connexion serveur n'a pas été initialisé")

        # écoute et démarrage d'acception des clients
        server.server.listen()

        try:
            count_of_client = 0

            while True:
                print(f">> Attente du client {count_of_client}")

                conn, _ = server.server.accept()

                # lancement du thread client
                server_client_manager(conn, count_of_client).start()

                print(f"\tClient({count_of_client}) lancé")
                count_of_client += 1

        except Exception as _:
            raise communication_exception("Une erreur s'est produite lors de l'acceptation de clients")


try:
    server.launch_server()
    server.accept_clients()
except communication_exception as e:
    print(e.get_error_message())
