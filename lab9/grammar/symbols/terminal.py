import re

import pytest

from lab9.grammar.symbols.symbol import Symbol


class Terminal(Symbol):
    """
        Class that represents a context-free grammar (CFG) terminal.
    """

    def __init__(self, symbol: str):
        super(Terminal, self).__init__(symbol)
        self.__terminal = 'terminal'

    @staticmethod
    def check_symbol(s: str) -> bool:
        return re.match('[^A-Z]+', s) is not None

    def __repr__(self):
        return f"t:{self._symbol}"


@pytest.mark.parametrize(
    "a,b,result",
    [
        (Terminal('a'), Symbol('a'), False),
        (Terminal('a'), Terminal('a'), True),
        (Terminal('a'), Terminal('b'), False),
        (Symbol('a'), Terminal('a'), False)
    ]
)
def test__eq__(a, b, result):
    assert (a == b) == result


if __name__ == '__main__':
    pytest.main([__file__])
