##
# @brief class de gestion des clients du serveur
import os
import socket
import threading
from communication_exception import communication_exception
from communication_config import communication_config


class server_client_manager(threading.Thread):
    ##
    # @brief action pour récupérer la liste des ressources
    get_ressources_list = "1"

    ##
    # @brief fermeture de connexion
    close_connection = "2"

    ##
    # @brief chemin des ressources
    resources_path = "../resources"

    ##
    # numéro du client
    my_number = -1

    ##
    # @param conn connexion socket de client lié
    # @param my_number numéro du client
    def __init__(self, conn: socket.SocketType, my_number: int):
        super().__init__()
        self.conn = conn
        self.my_number = my_number

    def run(self):
        try:
            while True:
                action = self.conn.recv(3).decode()

                if action == server_client_manager.get_ressources_list:
                    self.get_ressources_lists()
                elif action == server_client_manager.close_connection:
                    print(f">> Deconnexion du client({self.my_number})")
                    self.conn.close()
                    break
        except Exception as _:
            raise communication_exception("Echec de réception du message client")

    ##
    # @brief récupère la liste des ressources
    def get_ressources_lists(self):
        for r, d, f in os.walk(server_client_manager.resources_path):
            for file in f:
                complete_path = f"{r}/{file}".replace("\\", "/").encode()

                self.send_future_message_len(complete_path)
                self.conn.send(complete_path)

        end_message = communication_config.message_ending.encode()

        self.send_future_message_len(end_message)
        self.conn.send(end_message)

    ##
    # @brief envoi la taille du futur message
    # @param future_send le message futur
    def send_future_message_len(self, future_send: bytes):
        print("taille : " + str(len(future_send)))
        self.conn.send(str(len(future_send)).encode())
