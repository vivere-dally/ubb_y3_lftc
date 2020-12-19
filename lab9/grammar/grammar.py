from typing import List, Dict, Set
from uuid import uuid1, UUID
import re

from lab9.grammar.production_rule import ProductionRule
from lab9.grammar.symbols.dollar import Dollar
from lab9.grammar.symbols.epsilon import Epsilon
from lab9.grammar.symbols.nonterminal import Nonterminal
from lab9.grammar.symbols.symbol import Symbol
from lab9.grammar.symbols.terminal import Terminal


class Grammar:
    """
        Class that represents a context-free grammar (CFG).
    """

    def __init__(self, nonterminals: List[Nonterminal], terminals: List[Terminal],
                 production_rules: List[ProductionRule]):
        self.__nonterminals = nonterminals
        self.__terminals = terminals
        self.__production_rules = production_rules
        self.__start_symbol = self.__production_rules[0].lhs

    # region Getters and Setters

    @property
    def nonterminals(self) -> List[Nonterminal]:
        return self.__nonterminals

    @property
    def terminals(self) -> List[Terminal]:
        return self.__terminals

    @property
    def production_rules(self) -> List[ProductionRule]:
        return self.__production_rules

    @property
    def start_symbol(self) -> Nonterminal:
        return self.__start_symbol

    # endregion

    def __repr__(self):
        newline = '\n'
        return f"Nonterminals: {', '.join(repr(nonterminal) for nonterminal in self.__nonterminals)}\n" + \
               f"Terminals: {', '.join(repr(terminal) for terminal in self.__terminals)}\n" + \
               f"Production rules:\n{newline.join(repr(production_rule) for production_rule in self.__production_rules)}\n "

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
