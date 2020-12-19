import re

import pytest

from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal


class Nonterminal(Symbol):
    """
        Class that represents a context-free grammar (CFG) nonterminal.
    """

    def __init__(self, symbol: str):
        super(Nonterminal, self).__init__(symbol)
        self.__nonterminal = 'NONTERMINAL'

    @staticmethod
    def check_symbol(s: str) -> bool:
        return re.match("[A-Z_']+", s) is not None and s.isupper()

    def __repr__(self):
        return f'T:{self._symbol}'


@pytest.mark.parametrize(
    "a,b,result",
    [
        (Nonterminal('A'), Symbol('A'), False),
        (Symbol('A'), Nonterminal('A'), False),
        (Nonterminal('A'), Terminal('a'), False),
        (Terminal('a'), Nonterminal('A'), False),
        (Nonterminal('A'), Nonterminal('A'), True),
        (Nonterminal("A'"), Nonterminal("A'"), True),
        (Nonterminal("A_'"), Nonterminal("A_'"), True),
        (Nonterminal('A'), Nonterminal('B'), False)
    ]
)
def test__eq__(a, b, result):
    assert (a == b) == result


if __name__ == '__main__':
    pytest.main([__file__])
