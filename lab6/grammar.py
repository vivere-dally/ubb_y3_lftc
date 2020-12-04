class Grammar:
    def __init__(self, nonterminals: str, terminals: str, production_rules: dict):
        """
        Args:
            nonterminals (string): String of nonterminals. One character represents a nonterminal.
            terminals (string): String of terminals. One character represents a terminal.
            production_rules (dict<string,list<string>>): Dict of production rules. The key is a nonterminal that contains a list of possible patterns that it generates.
        """

        self.__nonterminals = nonterminals
        self.__terminals = terminals
        self.__production_rules = production_rules

    def __remove_redundant_production_rules(self):
        pass

    def get_production_rules_by_nonterminal(self, nonterminal: str) -> list:
        matching_production_rules = []
        if nonterminal not in self.__nonterminals:
            return []

        for k, v in self.__production_rules.items():
            if nonterminal in k:
                for v_ in v:
                    matching_production_rules.append('->'.join([k, v_]))

        return matching_production_rules
