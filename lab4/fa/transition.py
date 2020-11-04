class Transition:
    """Class that represents a transition suffix i.e. the secondary state and the necessary symbols to get to this state.
    """

    def __init__(self, state: str, symbols: list):
        """Initializes a transition class.
        Args:
            state (str): the state e.g. q2
            symbols (list<str>): the needed symbols to get to this state e.g. 3
        """
        self.state = state
        self.symbols = symbols

    def __repr__(self):
        return f"to {self.state} with {self.symbols}"
