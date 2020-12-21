from uuid import uuid1

import pytest

from lab9.grammar.production_rule import ProductionRule
from lab9.grammar.symbols.epsilon import Epsilon
from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal


class LR0Item:
    """
    Class that represents a CFG LR0 Item. A LR0 item is a production rule from a closure which has a dot in the
    right-hand side. The dot represents how many symbols were resolved.
    E.g.:
        1) S->.abc
           No symbol was resolved for this production rule.

        2) S->a.bc
           Only a was resolved.

        3) S->abc.
           The whole production rule was resolved.

    """

    def __init__(self, production_rule: ProductionRule):
        if len(production_rule.rhs) == 0:
            raise RuntimeError('RHS cannot be empty.')

        self.__production_rule = production_rule
        self.__dot_index = 0

    @property
    def production_rule(self) -> ProductionRule:
        return self.__production_rule

    @property
    def dot_index(self) -> int:
        return self.__dot_index

    @property
    def current_symbol(self) -> Symbol:
        return self.__production_rule.rhs[self.__dot_index]

    @property
    def is_final_item(self) -> bool:
        return self.__dot_index == len(self.__production_rule.rhs) or self.current_symbol == Epsilon()

    def can_solve(self, symbol: Symbol) -> bool:
        if self.__production_rule.rhs[self.__dot_index] == symbol:
            return True

        return False

    def solve(self, symbol: Symbol) -> 'LR0Item':
        if not self.can_solve(symbol):
            raise RuntimeError(f'Cannot solve with {symbol}')

        item = LR0Item(self.__production_rule)
        item.__dot_index = self.__dot_index + 1
        return item

    def __eq__(self, other) -> bool:
        return isinstance(other, LR0Item) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__production_rule)

    def __repr__(self) -> str:
        return f'{repr(self.__production_rule)} with dot at {self.__dot_index}'

    def __str__(self) -> str:
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
    a_lr0 = LR0Item(a)
    b = ProductionRule(Nonterminal(b_lhs), b_rhs_terminals, test_id)
    b_lr0 = LR0Item(b)

    assert (a_lr0 == b_lr0) == result


if __name__ == '__main__':
    pytest.main([__file__])
