from typing import List
from uuid import uuid1, UUID
import re


class Symbol:
    """
        Class that represents a context-free grammar (CFG) symbol.
    """

    def __init__(self, symbol: str):
        self._symbol = symbol

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._symbol = value

    def __str__(self):
        return repr(self)


class Terminal(Symbol):
    """
        Class that represents a context-free grammar (CFG) terminal.
    """

    def __init__(self, symbol: str):
        super(Terminal, self).__init__(symbol)

    @staticmethod
    def is_terminal(s: str) -> bool:
        return re.match('[a-z_]+', s) is not None and s.islower()

    def __eq__(self, other) -> bool:
        return isinstance(other, Terminal) and self._symbol == other._symbol

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self):
        return hash(self._symbol)

    def __repr__(self):
        return f't:{self._symbol}'


class Nonterminal(Symbol):
    """
        Class that represents a context-free grammar (CFG) nonterminal.
    """

    def __init__(self, symbol: str):
        super(Nonterminal, self).__init__(symbol)

    @staticmethod
    def is_nonterminal(s: str) -> bool:
        return re.match('[A-Z_]+', s) is not None and s.isupper()

    def __eq__(self, other) -> bool:
        return isinstance(other, Nonterminal) and self._symbol == other._symbol

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self):
        return hash(self._symbol)

    def __repr__(self):
        return f'T:{self._symbol}'


class Epsilon(Symbol):
    """
        Class that represents an epsilon.
    """

    def __init__(self):
        super(Epsilon, self).__init__("epsilon")

    @staticmethod
    def is_epsilon(s: str) -> bool:
        return s == "epsilon"

    def __eq__(self, other) -> bool:
        return isinstance(other, Epsilon) and self._symbol == other._symbol

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self):
        return hash(self._symbol)

    def __repr__(self):
        return f'{self._symbol}'


class ProductionRule:
    """
        Class that represents a context-free grammar (CFG) production rule.
    """

    def __init__(self, lhs: Nonterminal, rhs: List[Symbol]):
        self.__id = uuid1()
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
        return isinstance(other, ProductionRule) and self.__lhs == other.__lhs and self.__rhs == other.__rhs

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self):
        return hash(self.__id)

    def __repr__(self):
        return f'{repr(self.__lhs)}->{" ".join([repr(symbol) for symbol in self.__rhs])}'

    def __str__(self):
        return repr(self)


class Grammar:
    """
        Class that represents a context-free grammar (CFG).
    """

    def __init__(self, nonterminals: List[Nonterminal], terminals: List[Terminal], production_rules: List[ProductionRule]):
        self.__nonterminals = nonterminals
        self.__terminals = terminals
        self.__production_rules = production_rules

# region Getters and Setters

    @property
    def nonterminals(self) -> List[Nonterminal]:
        return self.__nonterminals

    @nonterminals.setter
    def nonterminals(self, value: List[Nonterminal]):
        self.__nonterminals = value

    @property
    def terminals(self) -> List[Terminal]:
        return self.__terminals

    @terminals.setter
    def terminals(self, value: List[Terminal]):
        return self.__terminals

    @property
    def production_rules(self) -> List[ProductionRule]:
        return self.__production_rules

    @production_rules.setter
    def production_rules(self, value: List[ProductionRule]):
        self.__production_rules = value

# endregion

    def __repr__(self):
        newline = '\n'
        return f"Nonterminals: {', '.join(repr(nonterminal) for nonterminal in self.__nonterminals)}\n" + \
            f"Terminals: {', '.join(repr(terminal) for terminal in self.__terminals)}\n" + \
            f"Production rules:\n{newline.join(repr(production_rule) for production_rule in self.__production_rules)}\n"

    def __str__(self):
        return repr(self)

    def get_production_rules_by_lhs_nonterminal(self, nonterminal: Nonterminal) -> List[ProductionRule]:
        """
            Return all production rules that have as lhs the given nonterminal.

        Args:
            nonterminal (Nonterminal): The query nonterminal

        Returns:
            List[ProductionRule]: All the production rules that have as lhs the query nonterminal
        """

        matching_production_rules = []
        if nonterminal not in self.__nonterminals:
            return []

        for production_rule in self.__production_rules:
            if production_rule.lhs == nonterminal:
                matching_production_rules.append(production_rule)

        return matching_production_rules

    def get_production_rules_by_rhs_nonterminal(self, nonterminal: Nonterminal) -> List[ProductionRule]:
        """
            Return all production rules that have as rhs the given nonterminal.

        Args:
            nonterminal (Nonterminal): The query nonterminal

        Returns:
            List[ProductionRule]: All the production rules that have as rhs the query nonterminal
        """

        matching_production_rules = []
        if nonterminal not in self.__nonterminals:
            return []

        for production_rule in self.__production_rules:
            if nonterminal in production_rule.rhs:
                matching_production_rules.append(production_rule)

        return matching_production_rules

    def get_production_rules_by_rhs_terminal(self, terminal: Terminal) -> List[ProductionRule]:
        """
            Return all production rules that have as rhs the given terminal.

        Args:
            terminal (Nonterminal): The query terminal

        Returns:
            List[ProductionRule]: All the production rules that have as rhs the query terminal
        """

        matching_production_rules = []
        if terminal not in self.__terminals:
            return []

        for production_rule in self.__production_rules:
            if terminal in production_rule.rhs:
                matching_production_rules.append(production_rule)

        return matching_production_rules