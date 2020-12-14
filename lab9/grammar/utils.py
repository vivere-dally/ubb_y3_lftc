from grammar.grammar import Grammar, Terminal, Nonterminal, Epsilon, ProductionRule


class LoadGrammarError(RuntimeError):
    """
        Error thrown when the given input file is not a correct context-free grammar (CFG).
    """

    def __init__(self):
        super().__init__('Bad input file.\nThe given grammar is not a context-free grammar (CFG).')


def load_grammar(path: str) -> Grammar:
    """
        Load a CFG from file.

    Args:
        path (str): Path to the CFG file

    Returns:
        Grammar: Returns a new CFG.
    """

    nonterminals = set()
    terminals = set()
    production_rules = []
    try:
        with open(path) as fin:
            for line in fin:
                line = line.strip().rstrip()
                if line:
                    lhs, rhs = line.split('->')
                    if not Nonterminal.is_nonterminal(lhs) or Epsilon.is_epsilon(lhs):
                        raise LoadGrammarError()

                    lhs_nonterminal = Nonterminal(lhs)
                    nonterminals.add(lhs_nonterminal)
                    rhs = rhs.split('|')  # Compact production rule
                    for rhs_ in rhs:
                        rhs_ = rhs_.split(' ')  # Multiple symbols
                        rhs_list = []
                        for rhs__ in rhs_:
                            if Epsilon.is_epsilon(rhs__):
                                # Add to current production rule rhs list
                                rhs_list.append(Epsilon())
                            elif Nonterminal.is_nonterminal(rhs__):
                                nonterminal = Nonterminal(rhs__)
                                # Add to nonterminals set
                                nonterminals.add(nonterminal)
                                # Add to current production rule rhs list
                                rhs_list.append(nonterminal)
                            elif Terminal.is_terminal(rhs__):
                                terminal = Terminal(rhs__)
                                # Add to terminals set
                                terminals.add(terminal)
                                # Add to current production rule rhs list
                                rhs_list.append(terminal)
                            else:
                                raise LoadGrammarError()

                        production_rules.append(
                            ProductionRule(lhs_nonterminal, rhs_list))

    except Exception:
        raise LoadGrammarError()

    return Grammar(list(nonterminals), list(terminals), production_rules)
