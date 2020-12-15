import os

from typing import List

from grammar.utils import load_grammar
from lab9.grammar.grammar import Grammar, Nonterminal, Symbol, Epsilon, Terminal
from lab9.slr.slr import SLR


def parse_line(sequence: str) -> List[Symbol]:
    symbols = []
    for seq in sequence.split(' '):
        if Epsilon.is_epsilon(seq):
            symbols.append(Epsilon())
        elif Nonterminal.is_nonterminal(seq):
            symbols.append(Nonterminal(seq))
        elif Terminal.is_terminal(seq):
            symbols.append(Terminal(seq))
        else:
            raise RuntimeError('BAD INPUT!')

    return symbols


if __name__ == '__main__':
    grammar_path = os.path.join(os.getcwd(), 'grammars', 'fifth-test.in')
    grammar: Grammar = load_grammar(grammar_path)
    grammar.compute_first_wrapper()
    grammar.compute_follow_wrapper()
    print(repr(grammar))
    print(grammar.first)
    print(grammar.follow)
    slr = SLR(grammar)
    print()

    menu = "\n\nSequence to be checked\n>> "
    while True:
        line = input(menu)
        if not line:
            break

        print(slr.parse(parse_line(line)))
