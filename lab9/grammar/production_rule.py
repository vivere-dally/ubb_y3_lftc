from typing import List
from uuid import uuid1, UUID

import pytest

from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal


class ProductionRule:
    """
        Class that represents a context-free grammar (CFG) production rule.
    """

    def __init__(self, lhs: Nonterminal, rhs: List[Symbol], production_rule_id: UUID = uuid1()):
        self.__id = production_rule_id
        self.__lhs = lhs
        self.__rhs = rhs

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def lhs(self) -> Nonterminal:
        return self.__lhs

    @property
    def rhs(self) -> List[Symbol]:
        return self.__rhs

    def __eq__(self, other) -> bool:
        return isinstance(other, ProductionRule) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__id)

    def __repr__(self):
        return f'{repr(self.__lhs)}->{" ".join([repr(symbol) for symbol in self.__rhs])}'

    def __str__(self):
        return repr(self)


@pytest.mark.parametrize(
    "a_lhs,a_rhs,b_lhs,b_rhs,result",
    [
        ('A', ['a', 'b', 'c'], 'A', ['a', 'b', 'c'], True),
        ('A', ['a', 'b', 'c'], 'A', ['a', 'a', 'c'], False)
    ]
)
def test__eq__(a_lhs, a_rhs, b_lhs, b_rhs, result):
    a_rhs_terminals = []
    b_rhs_terminals = []
    for a_rhs_, b_rhs_ in zip(a_rhs, b_rhs):
        a_rhs_terminals.append(Terminal(a_rhs_))
        b_rhs_terminals.append(Terminal(b_rhs_))

    test_id = uuid1()
    a = ProductionRule(Nonterminal(a_lhs), a_rhs_terminals, test_id)
    b = ProductionRule(Nonterminal(b_lhs), b_rhs_terminals, test_id)

    assert (a == b) == result


if __name__ == '__main__':
    pytest.main([__file__])
