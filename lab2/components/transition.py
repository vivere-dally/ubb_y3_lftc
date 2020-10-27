class Transition:
    """Class that represents a transition suffix i.e. the secondary state and the necessary number to get to this state.
    """

    def __init__(self, state: str, number: str):
        """Initializes a transition class.
        Args:
            state (str): the state e.g. q2
            number (str): the needed number to get to this state e.g. 3
        """
        self.state = state
        self.number = number

    def __repr__(self):
        return f"to {self.state} with {self.number}"
