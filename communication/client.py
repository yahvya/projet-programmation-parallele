import sys
sys.path.append("..")
sys.path.append("../communication")
sys.path.append("../huffman_compression")
import os
import threading
from termcolor import colored


from communication.transmission_manager import transmission_manager
from huffman_compression.huffman_compressor import huffman_compressor


##
# @brief gestionnaire client
class client(threading.Thread):
    ##
    # @brief récupération de la liste des fichiers
    get_files = "1"

    ##
    # @brief ferme la connexion
    close_con = "2"

    ##
    # @brief recevoir la liste des fichiers à télécharger
    receive_files_to_download_action = "3"

    ##
    # @brief erreur de compression sur le fichier
    compression_error = "4"

    ##
    # @brief nouveau fichier traité
    new_file = "5"

    ##
    # @brief réception de l'arbre
    receive_tree = "6"

    ##
    # @brief réception du contenu
    receive_content = "7"

    ##
    # @brief fin de compression d'un fichier
    compression_end = "8"

    ##
    # @brief fin de transmission
    transmission_end = "--end--"

    ##
    # @param con connexion
    # @param client_number numéro associé au client
    def __init__(self, con, client_number):
        super().__init__()
        self.con = con
        self.number = client_number

    def run(self):
        while True:
            action = transmission_manager.receive_string_message(self.con)

            if action == client.close_con:
                self.con.close()
                print(colored(f"\t>> Déconnexion du client ({self.number})", "blue"))
                break
            elif action == client.receive_files_to_download_action:
                self.receive_files_to_download()
            elif action == client.get_files:
                self.send_files_list()

    ##
    # @brief transmet la liste des fichiers
    def send_files_list(self) -> None:
        print(colored(f"\t\t>> Client ({self.number}) transmet la liste des fichiers", "grey"))

        ressources_path = "../ressources"

        for r, d, f in os.walk(ressources_path):
            for file in f:
                transmission_manager.send_string_message(self.con, f"{r}/{file}".replace("\\", "/"))

        transmission_manager.send_string_message(self.con, client.transmission_end)

    ##
    # @brief reçoit les fichiers à télécharger et lance le téléchargement
    def receive_files_to_download(self) -> None:
        path_to_download = []

        # récupération des chemins de fichiers à télécharger
        while True:
            data = transmission_manager.receive_string_message(self.con)

            if data == client.transmission_end:
                break

            if os.path.isfile(data):
                path_to_download.append(data)

        # compression des fichiers
        for path in path_to_download:
            print(colored(f"\t\t>> Compression du fichier {path}", "blue"))
            # envoi du chemin du fichier compressé
            transmission_manager.send_string_message(self.con, client.new_file)
            transmission_manager.send_string_message(self.con, path)
            # compression
            huffman_compressor(
                filepath=path,
                to_do_on_compression_error=lambda error: (
                    # envoi du message d'erreur
                    transmission_manager.send_string_message(self.con, client.compression_error),
                    transmission_manager.send_string_message(self.con, error.get_error_message())
                ),
                to_do_on_tree_build=lambda tree: (
                    # envoi de l'arbre compressé
                    transmission_manager.send_string_message(self.con, client.receive_tree),
                    transmission_manager.send_string_message(self.con, tree)
                ),
                to_do_on_block_build=lambda block: (
                    # envoi d'un block compressé
                    transmission_manager.send_string_message(self.con, client.receive_tree),
                    transmission_manager.send_string_message(self.con, block)
                ),
                to_do_on_compression_end=lambda count_of_added_zeros: (
                    # envoi de la fin de compression avec le nombre de 0 ajouté
                    transmission_manager.send_string_message(self.con, client.compression_end),
                    transmission_manager.send_string_message(self.con, str(count_of_added_zeros))
                )
            ).compress()

        transmission_manager.send_string_message(self.con, client.transmission_end)



