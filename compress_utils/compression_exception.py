class compression_exception(Exception):

    ##
    # @param error_message le message d'erreur
    # @param is_displayable si l'erreur peut être affichée
    def __init__(self, error_message: str, is_displayable: bool = True):
        super().__init__(error_message)

        self.is_displayable = is_displayable

    ##
    # @param default_message message d'erreur par défaut
    # @return le message d'erreur s'il peut être affiché ou un message par défaut
    def get_error_message(self, default_message: str = "Une erreur s'est produite") -> str:
        return str(self) if self.is_displayable else default_message
