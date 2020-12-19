import pytest

from lab9.grammar.symbols.symbol import Symbol


class Dollar(Symbol):
    def __init__(self):
        super(Dollar, self).__init__('$')
        self.__dollar = '$'

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s == "$"


@pytest.mark.parametrize(
    "a,b,result",
    [
        (Dollar(), Symbol('$'), False),
        (Dollar(), Dollar(), True),
        (Symbol('$'), Dollar(), False)
    ]
)
def test__eq__(a, b, result):
    assert (a == b) == result


if __name__ == '__main__':
    pytest.main([__file__])
