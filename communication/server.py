import sys
sys.path.append("..")
sys.path.append("../communication")

from termcolor import colored
import socket

from communication.client import client


##
# @brief gestion de serveur
class server:
    ##
    # @brief adresse de connexion
    address = "localhost"

    ##
    # @brief port de connexion
    port = 5555

    ##
    # @brief lance le serveur
    @staticmethod
    def launch():
        client_count = 0
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        con.bind((server.address, server.port))
        con.listen()

        print(colored("--- Lancement du serveur (attente des clients) ---\n", "green"))

        while True:
            client_con, _ = con.accept()
            client_count += 1

            client(client_con, client_count + 1).start()
            print(colored(f"\t>> Lancement du client ({client_count})", "blue"))


if __name__ == "__main__":
    server.launch()