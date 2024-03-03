import socket


##
# @brief gestionnaire de transmission
class transmission_manager:
    ##
    # @brief séparateur de message
    message_separator: str = "|"

    ##
    # @return le message récupéré directement au format d'octets
    @staticmethod
    def receive_byte_message(con: socket.SocketType) -> bytes:
        # récupération de la taille
        size = ""

        while True:
            char = con.recv(1).decode()

            if char == transmission_manager.message_separator:
                break

            size += char

        return con.recv(int(size))

    ##
    # @return le message récupéré directement au format de chaine
    @staticmethod
    def receive_string_message(con: socket.SocketType) -> str:
        return transmission_manager.receive_byte_message(con).decode()

    ##
    # @brief envoi un message d'octets
    # @param con la connexion
    # @param data la donnée à transmettre
    @staticmethod
    def send_byte_message(con: socket.SocketType, data: bytes) -> None:
        con.send(f"{str(len(data))}{transmission_manager.message_separator}".encode())
        con.send(data)

    ##
    # @brief envoi un message de chaine de caractères
    # @param con la connexion
    # @param data la donnée à transmettre
    @staticmethod
    def send_string_message(con: socket.SocketType, data: str) -> None:
        transmission_manager.send_byte_message(con, data.encode())
