import pytest

from lab9.grammar.symbols.symbol import Symbol


class Epsilon(Symbol):
    """
        Class that represents an epsilon.
    """

    def __init__(self):
        super(Epsilon, self).__init__("epsilon")
        self.__epsilon = 'epsilon'

    @staticmethod
    def check_symbol(s: str) -> bool:
        return s == "epsilon"


@pytest.mark.parametrize(
    "a,b,result",
    [
        (Epsilon(), Symbol('epsilon'), False),
        (Epsilon(), Epsilon(), True),
        (Symbol('epsilon'), Epsilon(), False)
    ]
)
def test__eq__(a, b, result):
    assert (a == b) == result


if __name__ == '__main__':
    pytest.main([__file__])
