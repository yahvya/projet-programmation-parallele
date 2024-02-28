##
# @brief class de configuration partagée pour la communication
class communication_config:
    ##
    # @brief adresse de connexion
    address = "localhost"

    ##
    # @brief port de connexion
    port = 5555

    ##
    # @brief symbole de fin d'envoi de message
    message_ending = "--end--"

    ##
    # @brief nouveau fichier
    new_file = "--new-file--"

    ##
    # @brief réception d'une partie du nouveau fichier
    receive_file_part = "--file_part--"
