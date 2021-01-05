from typing import Dict, Set

import pytest

from lab9.grammar.grammar import Grammar
from lab9.grammar.production_rule import ProductionRule
from lab9.grammar.symbols.dollar import Dollar
from lab9.grammar.symbols.epsilon import Epsilon
from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal


class FnF:
    """
        Class that represents a context-free grammar (CFG).
    """

    def __init__(self, grammar: Grammar):
        self.__grammar = grammar
        self.__first: Dict[Nonterminal, Set[Symbol]] = {}
        self.__follow: Dict[Nonterminal, Set[Symbol]] = {}
        self.__compute_first()
        self.__compute_follow()

    def __compute_first(self):
        def __compute_first__(nt: Nonterminal):
            if nt in computed_already:
                return

            nt_first = set()
            for pr in self.__grammar.get_production_rules_by_lhs_nonterminal(nt):
                for symbol in pr.rhs:
                    if isinstance(symbol, Epsilon) or isinstance(symbol, Terminal):
                        nt_first.add(symbol)
                        break
                    elif isinstance(symbol, Nonterminal) and symbol != nt:
                        if symbol not in computed_already:
                            __compute_first__(symbol)

                        s_first = self.get_first_of_nonterminal(symbol).copy()
                        if epsilon not in s_first:
                            nt_first = nt_first.union(s_first)
                            break
                        else:
                            s_first.remove(epsilon)
                            nt_first = nt_first.union(s_first)
                            if symbol == pr.rhs[-1]:
                                if pr.lhs not in computed_already and pr.lhs != nt:
                                    __compute_first__(pr.lhs)

                                lhs_first = self.get_first_of_nonterminal(pr.lhs).copy()
                                if len(lhs_first) == 0:
                                    nt_first.add(Epsilon())
                                else:
                                    nt_first = nt_first.union(lhs_first)

            computed_already.add(nt)
            self.__first[nt] = nt_first

        epsilon = Epsilon()
        computed_already = set()
        for nonterminal in self.__grammar.nonterminals:
            __compute_first__(nonterminal)

    def __compute_follow(self):
        def __split_rhs_by_duplicate_nonterminal__(pr: ProductionRule, nt: Nonterminal):
            counter = 0
            for s in pr.rhs:
                if s == nt:
                    counter += 1

            if counter == 1:
                return [pr]

            prs = []
            rhs = []
            for i in range(len(pr.rhs) - 1, -1, -1):
                rhs.insert(0, pr.rhs[i])
                if pr.rhs[i] == nt:
                    prs.append(ProductionRule(pr.lhs, rhs[:]))

            return prs

        def __compute_follow__(nt: Nonterminal):
            if nt in computed_already:
                return

            nt_follow = self.get_follow_of_nonterminal(nt)  # $ is added beforehand
            for pr in self.__grammar.get_production_rules_by_rhs_nonterminal(nt):
                for __pr__ in __split_rhs_by_duplicate_nonterminal__(pr, nt):
                    found_nt = False
                    rhs = []
                    for symbol in __pr__.rhs:
                        if found_nt:
                            rhs.append(symbol)

                        if symbol == nt:
                            found_nt = True

                    check_lhs = True
                    for symbol in rhs:
                        if isinstance(symbol, Terminal):
                            nt_follow.add(symbol)
                            check_lhs = False
                            break
                        elif isinstance(symbol, Nonterminal):
                            s_first = self.get_first_of_nonterminal(symbol).copy()
                            if epsilon not in s_first:
                                nt_follow = nt_follow.union(s_first)
                                if symbol != rhs[-1]:
                                    check_lhs = False
                                    break
                            else:
                                s_first.remove(epsilon)
                                nt_follow = nt_follow.union(s_first)
                                check_lhs = True

                    if check_lhs:
                        if __pr__.lhs not in computed_already and __pr__.lhs != nt:
                            __compute_follow__(__pr__.lhs)

                        lhs_follow = self.get_follow_of_nonterminal(__pr__.lhs).copy()
                        nt_follow = nt_follow.union(lhs_follow)

            computed_already.add(nt)
            self.__follow[nt] = nt_follow

        epsilon = Epsilon()
        computed_already = set()
        self.__follow[self.__grammar.start_symbol] = {Dollar()}
        for nonterminal in self.__grammar.nonterminals:
            __compute_follow__(nonterminal)

    # region Getters

    @property
    def first(self) -> Dict[Nonterminal, Set[Symbol]]:
        return self.__first

    @property
    def follow(self) -> Dict[Nonterminal, Set[Symbol]]:
        return self.__follow

    # endregion

    def __repr__(self):
        newline = '\n'
        return f"=== First ===\n{newline.join([repr(entry) for entry in self.__first.items()])}\n\n" \
               f"=== Follow ===\n{newline.join([repr(entry) for entry in self.__follow.items()])} "

    def __str__(self):
        return repr(self)

    def get_first_of_nonterminal(self, nonterminal: Nonterminal) -> Set[Symbol]:
        if nonterminal in self.__first:
            return self.__first[nonterminal]

        return set()

    def get_follow_of_nonterminal(self, nonterminal: Nonterminal) -> Set[Symbol]:
        if nonterminal in self.__follow:
            return self.__follow[nonterminal]

        return set()


@pytest.mark.parametrize(
    "grammar,first,follow",
    [
        (
                Grammar(
                    [
                        Nonterminal('S'),
                        Nonterminal('B'),
                        Nonterminal('D'),
                        Nonterminal('C'),
                        Nonterminal('E'),
                        Nonterminal('F')
                    ],
                    [
                        Terminal('a'),
                        Terminal('h'),
                        Terminal('c'),
                        Terminal('b'),
                        Terminal('g'),
                        Terminal('f')
                    ],
                    [
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Terminal('a'),
                                           Nonterminal('B'),
                                           Nonterminal('D'),
                                           Terminal('h')
                                       ]),
                        ProductionRule(Nonterminal('B'),
                                       [
                                           Terminal('c'),
                                           Nonterminal('C')
                                       ]),
                        ProductionRule(Nonterminal('C'),
                                       [
                                           Terminal('b'),
                                           Nonterminal('C')
                                       ]),
                        ProductionRule(Nonterminal('C'),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('D'),
                                       [
                                           Nonterminal('E'),
                                           Nonterminal('F')
                                       ]),
                        ProductionRule(Nonterminal('E'),
                                       [
                                           Terminal('g')
                                       ]),
                        ProductionRule(Nonterminal('E'),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('F'),
                                       [
                                           Terminal('f')
                                       ]),
                        ProductionRule(Nonterminal('F'),
                                       [
                                           Epsilon()
                                       ])
                    ]),
                {
                    Nonterminal('S'): {Terminal('a')},
                    Nonterminal('B'): {Terminal('c')},
                    Nonterminal('C'): {Terminal('b'), Epsilon()},
                    Nonterminal('D'): {Terminal('g'), Terminal('f'), Epsilon()},
                    Nonterminal('E'): {Terminal('g'), Epsilon()},
                    Nonterminal('F'): {Terminal('f'), Epsilon()}
                },
                {
                    Nonterminal('S'): {Dollar()},
                    Nonterminal('B'): {Terminal('g'), Terminal('f'), Terminal('h')},
                    Nonterminal('C'): {Terminal('g'), Terminal('f'), Terminal('h')},
                    Nonterminal('D'): {Terminal('h')},
                    Nonterminal('E'): {Terminal('f'), Terminal('h')},
                    Nonterminal('F'): {Terminal('h')}
                }
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
                    ]),
                {
                    Nonterminal('S'): {Terminal('a')},
                    Nonterminal('A'): {Terminal('a')},
                    Nonterminal("A'"): {Terminal('d'), Epsilon()},
                    Nonterminal('B'): {Terminal('b')},
                    Nonterminal('C'): {Terminal('g')},
                },
                {
                    Nonterminal('S'): {Dollar()},
                    Nonterminal('A'): {Dollar()},
                    Nonterminal("A'"): {Dollar()},
                    Nonterminal('B'): {Terminal('d'), Dollar()},
                    Nonterminal('C'): set()
                }
        ),
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
                    ]),
                {
                    Nonterminal('S'): {Terminal('('), Terminal('a')},
                    Nonterminal('L'): {Terminal('('), Terminal('a')},
                    Nonterminal("L'"): {Terminal(','), Epsilon()}
                },
                {
                    Nonterminal('S'): {Dollar(), Terminal(","), Terminal(')')},
                    Nonterminal('L'): {Terminal(')')},
                    Nonterminal("L'"): {Terminal(')')}
                }
        ),
        (
                Grammar(
                    [
                        Nonterminal('S'),
                        Nonterminal('A'),
                        Nonterminal('B')
                    ],
                    [
                        Terminal('a'),
                        Terminal('b')
                    ],
                    [
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('A'),
                                           Terminal('a'),
                                           Nonterminal('A'),
                                           Terminal('b')
                                       ]),
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('B'),
                                           Terminal('b'),
                                           Nonterminal('B'),
                                           Terminal('a')
                                       ]),
                        ProductionRule(Nonterminal('A'),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('B'),
                                       [
                                           Epsilon()
                                       ])
                    ]),
                {
                    Nonterminal('S'): {Terminal('a'), Terminal('b')},
                    Nonterminal('A'): {Epsilon()},
                    Nonterminal('B'): {Epsilon()}
                },
                {
                    Nonterminal('S'): {Dollar()},
                    Nonterminal('A'): {Terminal('a'), Terminal('b')},
                    Nonterminal('B'): {Terminal('a'), Terminal('b')}
                }
        ),
        (
                Grammar(
                    [
                        Nonterminal('E'),
                        Nonterminal("E'"),
                        Nonterminal('T'),
                        Nonterminal("T'"),
                        Nonterminal('F'),
                    ],
                    [
                        Terminal('+'),
                        Terminal('*'),
                        Terminal('('),
                        Terminal(')'),
                        Terminal('id')
                    ],
                    [
                        ProductionRule(Nonterminal('E'),
                                       [
                                           Nonterminal('T'),
                                           Nonterminal("E'")
                                       ]),
                        ProductionRule(Nonterminal("E'"),
                                       [
                                           Terminal('+'),
                                           Nonterminal('T'),
                                           Nonterminal("E'")
                                       ]),
                        ProductionRule(Nonterminal("E'"),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('T'),
                                       [
                                           Nonterminal('F'),
                                           Nonterminal("T'")
                                       ]),
                        ProductionRule(Nonterminal("T'"),
                                       [
                                           Terminal('*'),
                                           Nonterminal('F'),
                                           Nonterminal("T'")
                                       ]),
                        ProductionRule(Nonterminal("T'"),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('F'),
                                       [
                                           Terminal('('),
                                           Nonterminal('E'),
                                           Terminal(')')
                                       ]),
                        ProductionRule(Nonterminal('F'),
                                       [
                                           Terminal('id')
                                       ])
                    ]),
                {
                    Nonterminal('E'): {Terminal('('), Terminal('id')},
                    Nonterminal("E'"): {Terminal('+'), Epsilon()},
                    Nonterminal('T'): {Terminal('('), Terminal('id')},
                    Nonterminal("T'"): {Terminal('*'), Epsilon()},
                    Nonterminal('F'): {Terminal('('), Terminal('id')}
                },
                {
                    Nonterminal('E'): {Dollar(), Terminal(')')},
                    Nonterminal("E'"): {Dollar(), Terminal(')')},
                    Nonterminal('T'): {Terminal('+'), Dollar(), Terminal(')')},
                    Nonterminal("T'"): {Terminal('+'), Dollar(), Terminal(')')},
                    Nonterminal('F'): {Terminal('*'), Terminal('+'), Dollar(), Terminal(')')}
                }
        ),
        (
                Grammar(
                    [
                        Nonterminal('S'),
                        Nonterminal('A'),
                        Nonterminal('B'),
                        Nonterminal('C')
                    ],
                    [
                        Terminal('a'),
                        Terminal('b'),
                        Terminal('d'),
                        Terminal('g'),
                        Terminal('h')
                    ],
                    [
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('A'),
                                           Nonterminal('C'),
                                           Nonterminal('B')
                                       ]),
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('C'),
                                           Terminal('b'),
                                           Nonterminal('B')
                                       ]),
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('B'),
                                           Terminal('a')
                                       ]),
                        ProductionRule(Nonterminal('A'),
                                       [
                                           Terminal('d'),
                                           Terminal('a')
                                       ]),
                        ProductionRule(Nonterminal('A'),
                                       [
                                           Nonterminal('B'),
                                           Nonterminal('C')
                                       ]),
                        ProductionRule(Nonterminal('B'),
                                       [
                                           Terminal('g')
                                       ]),
                        ProductionRule(Nonterminal('B'),
                                       [
                                           Epsilon()
                                       ]),
                        ProductionRule(Nonterminal('C'),
                                       [
                                           Terminal('h')
                                       ]),
                        ProductionRule(Nonterminal('C'),
                                       [
                                           Epsilon()
                                       ])
                    ]),
                {
                    Nonterminal('S'): {Terminal('d'), Terminal('g'), Terminal('h'), Epsilon(), Terminal('b'),
                                       Terminal('a')},
                    Nonterminal('A'): {Terminal('d'), Terminal('g'), Terminal('h'), Epsilon()},
                    Nonterminal('B'): {Terminal('g'), Epsilon()},
                    Nonterminal('C'): {Terminal('h'), Epsilon()}
                },
                {
                    Nonterminal('S'): {Dollar()},
                    Nonterminal('A'): {Dollar(), Terminal('g'), Terminal('h')},
                    Nonterminal('B'): {Dollar(), Terminal('g'), Terminal('h'), Terminal('a')},
                    Nonterminal('C'): {Dollar(), Terminal('g'), Terminal('h'), Terminal('b')}
                }
        ),
        (
                Grammar(
                    [
                        Nonterminal('S'),
                        Nonterminal('A')
                    ],
                    [
                        Terminal('a'),
                        Terminal('b')
                    ],
                    [
                        ProductionRule(Nonterminal('S'),
                                       [
                                           Nonterminal('A'),
                                           Nonterminal('A'),
                                           Terminal('b')
                                       ]),
                        ProductionRule(Nonterminal('A'),
                                       [
                                           Terminal('a')
                                       ])
                    ]),
                {
                    Nonterminal('S'): {Terminal('a')},
                    Nonterminal('A'): {Terminal('a')}
                },
                {
                    Nonterminal('S'): {Dollar()},
                    Nonterminal('A'): {Terminal('a'), Terminal('b')}
                }
        )
    ]
)
def test__fnf__(grammar, first, follow):
    fnf = FnF(grammar)
    assert fnf.first == first and fnf.follow == follow


if __name__ == '__main__':
    pytest.main([__file__])
