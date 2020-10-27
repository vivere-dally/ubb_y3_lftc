import components.transition as trans


class FiniteAutomaton:
    """Class that represents a finite automaton.
    """

    def __init__(self, alphabet: list, states: list, initial_state: str, final_states: list, transitions: dict):
        """Initializes a finite automaton class.

        Args:
            alphabet (list): a list of strings that represents the alphabet e.g. ["0", "1", "2"]
            states (list): a list of strings that represents all the states in the FA
            initial_state (str): a string that represents a state which is the entry point in the automaton. E.g. q0
            final_states (list): a list of strings that represent the final states. E.g. ["q0","q1","q2"]
            transitions (dict): a dictionary with key string and value list of components.transition.Transition. I.e. from state i you can go to states 1..n.
        """
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def __repr__(self):
        all_trans = ""
        for state in self.states:
            for transition in self.transitions.get(state, []):
                all_trans += f"\nfrom {state} {transition}"

        return f"States: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {all_trans}\nFinal states: {self.final_states}\n"

    def check_sequence(self, sequence: str) -> bool:
        """Checks if a sequence of numbers is accepted by the finite automaton.

        Args:
            sequence (str): the str of numbers to move from one state to another

        Returns:
            bool: true if the sequence is accepted, false otherwise
        """
        is_accepted = True
        current_state = self.initial_state
        for number in sequence:
            if number not in self.alphabet:
                print(f"{number} not in alphabet. Continue...")
                is_accepted = False
                continue

            current_state_changed = False
            for transition in self.transitions.get(current_state, []):
                if transition.number == number:
                    print(f"from {current_state} {transition}")
                    current_state = transition.state
                    current_state_changed = True
                    break

            if not current_state_changed:
                print(
                    f"no transition from {current_state} with {number}. Continue...")
                is_accepted = False

        if current_state not in self.final_states:
            return False

        return is_accepted

    def get_longest_prefix(self, sequence: str) -> str:
        """Returns the longest prefix of numbers that is accepted by the finite automaton.

        Args:
            sequence (str): the string of numbers to move from one state to another

        Returns:
            str: the longest prefix
        """
        current_state = self.initial_state
        prefix_end_index = 0
        for number in sequence:
            if number not in self.alphabet:
                break

            current_state_changed = False
            for transition in self.transitions.get(current_state, []):
                if transition.number == number:
                    current_state = transition.state
                    current_state_changed = True
                    break

            if not current_state_changed:
                break

            prefix_end_index += 1

        prefix = sequence[:prefix_end_index]
        while not prefix and not self.check_sequence(prefix):
            prefix = prefix[:-1]

        return prefix
