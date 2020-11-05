class UnexpectedTokenError(RuntimeError):
    """
        Error thrown when a token is not part of the MLP.
    """

    def __init__(self, line: int, line_index: int, token: str, message: str = ""):
        """
            Initialize UnexpectedTokenError

        Args:
            line (str): the line where the error was found
            line_index (index): the index on the line where the error was found
            token (str): the token at those indexes
            message (str, optional): Optional messages. Defaults to "".
        """
        self.__line = line
        self.__line_index = line_index
        self.__token = token
        self.__message = f"Unexpected token {token} on line {line} at {line_index}.\n{message}"
        super().__init__(self.__message)

    def __repr__(self):
        return f"Line: {self.__line}\nLine Index: {self.__line_index}\nToken: {self.__token}\n{super().__repr__()}"
