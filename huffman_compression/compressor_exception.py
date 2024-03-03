##
# @brief exception de compression
class compressor_exception(Exception):
    ##
    # @param error_message message d'erreur
    # @param is_displayable si le message peut être affiché
    def __init__(
            self,
            error_message: str,
            is_displayable: bool = True
    ):
        super().__init__(error_message)

        self.error_message = error_message
        self.is_displayable = is_displayable

    ##
    # @param default_message message par défaut si is_displayable est False
    # @return le message d'erreur associé s'il peut être affiché sinon le message par défaut
    def get_error_message(
            self,
            default_message: str = "Une erreur technique s'est produite"
    ) -> str:
        return self.error_message if self.is_displayable else default_message
