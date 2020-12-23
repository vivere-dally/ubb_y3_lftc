import random
from typing import List
from uuid import uuid1, UUID

import pytest

from lab9.grammar.grammar import Grammar
from lab9.grammar.production_rule import ProductionRule
from lab9.grammar.symbols.epsilon import Epsilon
from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal
from lab9.slr.lr0item import LR0Item


class Closure:
    """
    Class that represents a CFG closure. It is a collection of LR0 items
    """

    def __init__(self, grammar: Grammar, lr0items: List[LR0Item], closure_id: UUID = uuid1()):
        self.__grammar = grammar
        self.__lr0items = lr0items
        self.__apply_closure()

    def __apply_closure(self):
        def __apply_closure__(lr0item: LR0Item):
            if lr0item in lr0items \
                    or lr0item.is_final_item \
                    or not isinstance(lr0item.current_symbol, Nonterminal):
                return

            for pr in self.__grammar.get_production_rules_by_lhs_nonterminal(lr0item.current_symbol):
                new_lr0item = LR0Item(pr)
                if new_lr0item != lr0item:
                    __apply_closure__(new_lr0item)
                    if new_lr0item not in lr0items:
                        lr0items.append(new_lr0item)

        lr0items = []
        for item in self.__lr0items:
            __apply_closure__(item)

        self.__lr0items.extend(lr0items)

    @property
    def lr0items(self) -> List[LR0Item]:
        return self.__lr0items

    @property
    def is_final_closure(self) -> bool:
        for lr0item in self.__lr0items:
            if not (lr0item.is_final_item or lr0item.current_symbol == Epsilon()):
                return False

        return True

    @property
    def contains_epsilon(self) -> bool:
        epsilon = Epsilon()
        for lr0item in self.__lr0items:
            if epsilon in lr0item.production_rule.rhs:
                return True

        return False

    def __eq__(self, other) -> bool:
        return isinstance(other, Closure) and self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return sum([hash(item) for item in self.__lr0items])

    def __repr__(self):
        return '\n'.join([repr(item) for item in self.__lr0items])

    def __str__(self):
        return repr(self)


class ClosureTransition:
    def __init__(self, symbol: Symbol, from_index: int, to_index: int):
        self.__symbol = symbol
        self.__from_index = from_index
        self.__to_index = to_index

    @property
    def symbol(self) -> Symbol:
        return self.__symbol

    @property
    def from_index(self) -> int:
        return self.__from_index

    @property
    def to_index(self) -> int:
        return self.__to_index

    def __repr__(self):
        return f"from {self.__from_index} with {self.__symbol} to {self.__to_index}"

    def __str__(self):
        return repr(self)


# noinspection DuplicatedCode
@pytest.mark.parametrize(
    "grammar",
    [
        (
                Grammar(
                    [
                        Nonterminal('S'),
                        Nonterminal('L'),
                        Nonterminal("L'")
                    ],
                    [
                        Terminal('a'),
                        Terminal('('),
                        Terminal(')'),
                        Terminal(',')
                    ],
                    [
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Terminal('('),
                                           Nonterminal('L'),
                                           Terminal(')')
                                       ]),
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Terminal('a')
                                       ]),
                        ProductionRule(Nonterminal('L'),
                                       [
                                           Nonterminal('S'),
                                           Nonterminal("L'")
                                       ]),
                        ProductionRule(Nonterminal("L'"),
                                       [
                                           Terminal(','),
                                           Nonterminal('S'),
                                           Nonterminal("L'")
                                       ]),
                        ProductionRule(Nonterminal("L'"),
                                       [
                                           Epsilon()
                                       ])
                    ])
        ),
        (
                Grammar(
                    [
                        Nonterminal('S'),
                        Nonterminal('A'),
                        Nonterminal("A'"),
                        Nonterminal('B'),
                        Nonterminal('C')
                    ],
                    [
                        Terminal('a'),
                        Terminal('b'),
                        Terminal('d'),
                        Terminal('g')
                    ],
                    [
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('A')
                                       ]),
                        ProductionRule(Nonterminal('A'),
                                       [
                                           Terminal('a'),
                                           Nonterminal('B'),
                                           Nonterminal("A'")
                                       ]),
                        ProductionRule(Nonterminal("A'"),
                                       [
                                           Terminal('d'),
                                           Nonterminal("A'")
                                       ]),
                        ProductionRule(Nonterminal("A'"),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('B'),
                                       [
                                           Terminal('b')
                                       ]),
                        ProductionRule(Nonterminal('C'),
                                       [
                                           Terminal('g')
                                       ])
                    ])
        )
    ]
)
def test__eq__(grammar: Grammar):
    random_productions = [random.choice(grammar.production_rules) for _ in
                          range(random.randint(0, len(grammar.production_rules)))]

    lr0items = [LR0Item(pr) for pr in random_productions]
    closure_id = uuid1()
    assert Closure(grammar, lr0items, closure_id) == Closure(grammar, lr0items, closure_id)


if __name__ == '__main__':
    pytest.main([__file__])
