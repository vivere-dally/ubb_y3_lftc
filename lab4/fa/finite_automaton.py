from fa.transition import Transition
from fa.errors import SymbolNotInAlphabetError, TransitionNotFoundError


class FiniteAutomaton:
    """Class that represents a finite automaton.
    """

    def __init__(self, atom: str, alphabet: list, states: list, initial_state: str, final_states: list, transitions: dict):
        """Initializes a finite automaton class.

        Args:
            atom (str): the analyzed atom
            alphabet (list): a list of strings that represents the alphabet e.g. ["0", "1", "2"]
            states (list): a list of strings that represents all the states in the FA
            initial_state (str): a string that represents a state which is the entry point in the automaton. E.g. q0
            final_states (list): a list of strings that represent the final states. E.g. ["q0","q1","q2"]
            transitions (dict): a dictionary with key string and value list of fa.transition.Transition. I.e. from state i you can go to states 1..n.
        """
        self.atom = atom
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

        return f"Atom: {self.atom}\nStates: {self.states}\nAlphabet: {self.alphabet}\nTransitions: {all_trans}\nFinal states: {self.final_states}\n"

    def __get_next_state(self, symbol: str, state: str) -> (str, bool):
        """
            Get the next state

        Args:
            symbol (str): Specifies the symbol to move from the current state to the next one.e
            state (str): Specifies the current state.

        Returns:
            (str, bool): Returns a tuple formed from a str representing the state and a boolean representing wheter or not the state changed.
        """

        state_changed = False
        for transition in self.transitions.get(state, []):
            if symbol in transition.symbols:
                state = transition.state
                state_changed = True
                break

        return (state, state_changed)

    def check_sequence(self, sequence: list) -> bool:
        """
            Checks if a sequence of symbols is accepted by the finite automaton.

        Args:
            sequence (list): list of symbols to move from one state to another

        Returns:
            bool: true if the sequence is accepted, false otherwise
        """

        state = self.initial_state
        for symbol in sequence:
            if symbol not in self.alphabet:
                raise SymbolNotInAlphabetError(symbol, self.alphabet)

            state, state_changed = self.__get_next_state(symbol, state)
            if not state_changed:
                raise TransitionNotFoundError(symbol, state)

        if state not in self.final_states:
            return False

        return True

    def get_longest_prefix(self, sequence: list) -> str:
        """
            Returns the longest prefix of symbols that is accepted by the finite automaton.

        Args:
            sequence (list): list of symbols to move from one state to another

        Returns:
            str: the longest prefix
        """
        state = self.initial_state
        prefix_end_index = 0
        for symbol in sequence:
            if symbol not in self.alphabet:
                break

            state, state_changed = self.__get_next_state(symbol, state)
            if not state_changed:
                break

            prefix_end_index += 1

        prefix = sequence[:prefix_end_index]
        while prefix and not self.check_sequence(prefix):
            prefix = prefix[:-1]

        return prefix


def load_fa_from_file(path: str) -> FiniteAutomaton:
    """
        Reads the finite automaton from an input file that respects the ebnfs/finite_automaton.ebnf.

    Args:
        path (str): Path to the input file

    Returns:
        FiniteAutomaton: the finite automaton
    """

    alphabet = None
    states = set()
    initial_state = None
    final_states = None
    transitions = {}
    with open(path) as fin:
        atom = fin.readline().strip().rstrip()
        alphabet = fin.readline().strip().rstrip().split(';')
        initial_state = fin.readline().strip().rstrip()
        final_states = list(fin.readline().strip().rstrip().split(';'))
        for line in fin:
            prefix_state, sufix_state, symbols = line.strip().rstrip().split(';')
            states.add(prefix_state)
            states.add(sufix_state)
            symbols = list(symbols.split(','))
            if prefix_state in transitions:
                transitions[prefix_state].append(
                    Transition(sufix_state, symbols))
            else:
                transitions[prefix_state] = [
                    Transition(sufix_state, symbols)]

    states = sorted(list(states))
    return FiniteAutomaton(atom, alphabet, states, initial_state, final_states, transitions)


def load_fa_from_user() -> FiniteAutomaton:
    """
        Reads the finite automaton from the user input that respects the ebnfs/finite_automaton.ebnf.

    Returns:
        FiniteAutomaton: the finite automaton
    """

    atom = input("Enter the analyzed lexical atom:").strip().rstrip()
    alphabet = input(
        "Enter the alphabet (semicolon separated):").strip().rstrip().split(';')
    states = set()
    initial_state = input("Enter the initial state:").strip().rstrip()
    final_states = list(input(
        "Enter the final states (semicolon separated):").strip().rstrip().split(';'))
    transitions = {}
    print("Enter the transitions (from;to;symbols/symbol). E.g.: q0;q1;1,2,3. Press enter with an empty line to stop.")
    while True:
        line = input(">> ")
        if not line:
            break

        prefix_state, sufix_state, symbols = line.strip().rstrip().split(';')
        states.add(prefix_state)
        states.add(sufix_state)
        symbols = list(symbols.split(','))
        if prefix_state in transitions:
            transitions[prefix_state].append(
                Transition(sufix_state, symbols))
        else:
            transitions[prefix_state] = [
                Transition(sufix_state, symbols)]

    states = sorted(list(states))
    return FiniteAutomaton(atom, alphabet, states, initial_state, final_states, transitions)
