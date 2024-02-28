from communication_exception import communication_exception

##
# @brief gestionnaire de transmission de messages
import socket


class transmission_manager:
    ##
    # @brief séparateur de la taille du message suivant avec le réel message
    size_separator = "|"

    ##
    # @brief envoi un message
    # @throws communication_exception en cas d'erreur
    @staticmethod
    def send_message(conn: socket.SocketType,message: str) -> None:
        try:
            # formattage du message
            formatted_message = f"{len(message.encode())}{transmission_manager.size_separator}{message}"

            conn.send(formatted_message.encode())
        except Exception as _:
            raise communication_exception("Une erreur s'est produite lors de la transmission du message")

    ##
    # @brief récupère un message
    # @return le contenu du message
    # @throws communication_exception en cas d'erreur
    @staticmethod
    def receive_message_from(conn: socket.SocketType) -> [str,]:
        try:
            result = {"size": "", "message": None}

            while True:
                # récupération des différentes parties de la taille
                data = conn.recv(1).decode()

                if data == transmission_manager.size_separator:
                    # récupération du message
                    result["size"] = int(result["size"])
                    result["message"] = conn.recv(result["size"]).decode()

                    break
                else:
                    result["size"] += data

            return result
        except Exception as _:
            raise communication_exception("Une erreur s'est produite lros de la récupération du message")

