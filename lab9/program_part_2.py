import os

from typing import List

from grammar.utils import load_grammar
from lab9.slr.filters import is_left_recursive, is_deterministic
from lab9.slr.first_and_follow import FnF
from lab9.grammar.grammar import Grammar
from lab9.grammar.symbols.epsilon import Epsilon
from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal
from lab9.slr.slr import SLR


def parse_line(sequence: str) -> List[Symbol]:
    symbols = []
    for seq in sequence.split(' '):
        if Epsilon.check_symbol(seq):
            symbols.append(Epsilon())
        elif Nonterminal.check_symbol(seq):
            symbols.append(Nonterminal(seq))
        elif Terminal.check_symbol(seq):
            symbols.append(Terminal(seq))
        else:
            raise RuntimeError('BAD INPUT!')

    return symbols


if __name__ == '__main__':
    grammar_path = os.path.join(os.getcwd(), 'grammars', 'test.in')

    grammar: Grammar = load_grammar(grammar_path)
    print(repr(grammar))

    if not is_left_recursive(grammar):
        raise RuntimeError('The given grammar is left recursive!')

    if not is_deterministic(grammar):
        raise RuntimeError('The given grammar is non-deterministic!')

    fnf: FnF = FnF(grammar)
    print(repr(fnf))

    slr = SLR(grammar, fnf)

    menu = "\n\nSequence to be checked\n>> "
    while True:
        line = input(menu)
        if not line:
            break

        parsed_symbols = parse_line(line)
        result = slr.parse(parsed_symbols)
        print('\n'.join([str(r) for r in result]))
