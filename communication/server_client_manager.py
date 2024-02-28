import sys

sys.path.append("..")
sys.path.append("../compress_utils")

import os
import socket
import threading
from compress_utils.compression_exception import compression_exception
from communication_exception import communication_exception
from communication_config import communication_config
from transmission_manager import transmission_manager
from compress_utils.huffman_compressor import huffman_compressor


##
# @brief gestionnaire de thread client du serveur
class server_client_manager(threading.Thread):
    ##
    # @brief action pour récupérer la liste des ressources
    get_ressources_list = "1"

    ##
    # @brief fermeture de connexion
    close_connection = "2"

    ##
    # @brief récupération de fichier à télécharger
    get_files_to_download = "3"

    ##
    # @brief fin de transmission du chemin des fichiers
    end_filepath_sending = "4"

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
                # récupération de l'action à faire
                action = transmission_manager.receive_message_from(self.conn)["message"]

                if action == server_client_manager.close_connection:
                    self.disconnect_client()
                    break

                match = {
                    server_client_manager.get_ressources_list: lambda: self.get_ressources_lists(),
                    server_client_manager.get_files_to_download: lambda: self.receive_files_to_manage(),
                }

                if action in match:
                    match[action]()
        except Exception as e:
            print(e)
            raise communication_exception("Echec de réception du message client")

    ##
    # @brief envoi la liste des ressources, envoi la taille du message puis le message
    def get_ressources_lists(self):
        for r, d, f in os.walk(server_client_manager.resources_path):
            for file in f:
                transmission_manager.send_message(self.conn, f"{r}/{file}".replace("\\", "/"))

        transmission_manager.send_message(self.conn, communication_config.message_ending)

    ##
    # @brief récupère la liste des chemins de fichiers à envoyer, attend la réception de la taille puis le message
    def receive_files_to_manage(self):
        print("reception des fichiers à télécharger")
        files_path = []

        while True:
            # réception de la taille du futur message puis récupération du message
            data = transmission_manager.receive_message_from(self.conn)["message"]

            if data == self.end_filepath_sending:
                break

            files_path.append(data)

        # compression des fichiers
        for file_path in files_path:
            # envoi du nom du fichier actuellement traité
            transmission_manager.send_message(self.conn, communication_config.new_file)
            transmission_manager.send_message(self.conn, file_path)

            # compression du fichier
            try:
                transmission_manager.send_message(self.conn, communication_config.receive_file_part)
                transmission_manager.send_message(self.conn, "bonjour de test")
                huffman_compressor.compress_file(file_path)
            except compression_exception as e:
                transmission_manager.send_message(self.conn, communication_config.compression_error)
                transmission_manager.send_message(self.conn, e.get_error_message())

        transmission_manager.send_message(self.conn, communication_config.message_ending)

    ##
    # @brief déconnecte le client
    def disconnect_client(self):
        print(f">> Déconnexion du client({self.my_number})")
        self.conn.close()
