##
# @brief exception custom permettant l'ajout d'un statut message affichable ou non
class HuffmmanException(Exception):
    def __init__(self, error: str, is_displayable: bool):
        super(HuffmmanException, self).__init__(error)

        self.is_displayable = is_displayable

    ##
    # @return le message d'erreur s'il peut être affiché sinon le message par défaut
    def get_error_message(self) -> str:
        return str(self) if self.is_displayable else "Une erreur s'est produite"

    ##
    # @return si l'exception peut être affichée
    def get_is_displayable(self) -> bool:
        return self.is_displayable
