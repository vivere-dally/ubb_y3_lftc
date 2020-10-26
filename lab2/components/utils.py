import components.transition as trans
import components.finite_automaton as fa


def read_fa_from_file(path: str) -> fa.FiniteAutomaton:
    """Reads the finite automaton from an input file that respects the file_description.ebnf.

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
        alphabet = fin.readline().strip().rstrip().split(';')
        initial_state = fin.readline().strip().rstrip()
        final_states = fin.readline().strip().rstrip().split(';')
        for line in fin:
            prefix_state, sufix_state, number = line.strip().rstrip().split(';')
            states.add(prefix_state)
            states.add(sufix_state)
            if prefix_state in transitions:
                transitions[prefix_state].append(
                    trans.Transition(sufix_state, number))
            else:
                transitions[prefix_state] = [
                    trans.Transition(sufix_state, number)]

    states = sorted(list(states))
    return fa.FiniteAutomaton(alphabet, states, initial_state, final_states, transitions)


def read_fa_from_input() -> fa.FiniteAutomaton:
    """Reads the finite automaton from a user input that respects the file_description.ebnf.

    Returns:
        FiniteAutomaton: the finite automaton
    """
    alphabet = input(
        "Enter the alphabet (semicolon separated):").strip().rstrip().split(';')
    states = set()
    initial_state = input("Enter the initial state:").strip().rstrip()
    final_states = input(
        "Enter the final states (semicolon separated):").strip().rstrip().split(';')
    transitions = {}
    print("Enter the transitions (from;to;number). E.g.: q0;q1;1\nPress enter with an empty line to stop.")
    while True:
        line = input(">> ")
        if not line:
            break

        prefix_state, sufix_state, number = line.strip().rstrip().split(';')
        states.add(prefix_state)
        states.add(sufix_state)
        if prefix_state in transitions:
            transitions[prefix_state].append(
                trans.Transition(sufix_state, number))
        else:
            transitions[prefix_state] = [
                trans.Transition(sufix_state, number)]

    states = sorted(list(states))
    return fa.FiniteAutomaton(alphabet, states,  initial_state, final_states, transitions)
