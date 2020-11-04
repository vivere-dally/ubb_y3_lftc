class SymbolNotInAlphabetError(RuntimeError):
    """
        Error thrown when a character is not present in a finite automaton.
    """

    def __init__(self, symbol: str, alphabet: str, message: str = ""):
        """
            Initialize SymbolNotInAlphabetError

        Args:
            symbol (str): the query symbol
            alphabet (list<str>): the queried alphabet
            message (str, optional): Optional messages. Defaults to "".
        """
        self.__symbol = symbol
        self.__alphabet = alphabet
        self.__message = f"Symbol {symbol} not present in the alphabet {alphabet}.\n{message}"
        super().__init__(self.__message)

    def __repr__(self):
        return f"Symbol: {self.__symbol}\nAlphabet: {self.__alphabet}\n{super().__repr__()}"


class TransitionNotFoundError(RuntimeError):
    """
        Error thrown when a transition is not found between states.
    """

    def __init__(self, symbol: str, start_state: str, message: str = ""):
        """
            Initialize TransitionNotFoundError

        Args:
            symbol (str): the query symbol
            start_state (str): the starting state
            message (str, optional): Optional messages. Defaults to "".
        """
        self.__symbol = symbol
        self.__start_state = start_state
        self.__message = f"No transition found from {start_state} with symbol {symbol}.\n{message}"
        super().__init__(self.__message)

    def __repr__(self):
        return f"Symbol: {self.__symbol}\nStart state: {self.__start_state}\n{super().__repr__()}"
