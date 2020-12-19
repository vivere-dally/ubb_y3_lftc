import pytest


class Symbol:
    """
        Class that represents a context-free grammar (CFG) symbol.
    """

    def __init__(self, symbol: str):
        if not self.check_symbol(symbol):
            raise ValueError(f"Symbol {symbol} is not a {self.__class__.__name__}!")

        self._symbol = symbol

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._symbol = value

    @staticmethod
    def check_symbol(s: str) -> bool:
        return bool(s)

    def __repr__(self):
        return f"S:{self._symbol}"

    def __str__(self):
        return repr(self)

    def __eq__(self, other) -> bool:
        return isinstance(other, Symbol) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._symbol)


@pytest.mark.parametrize(
    "a,b,result",
    [
        (Symbol('a'), Symbol('a'), True),
        (Symbol('a'), Symbol('b'), False)
    ]
)
def test__eq__(a, b, result):
    assert (a == b) == result


if __name__ == '__main__':
    pytest.main([__file__])
