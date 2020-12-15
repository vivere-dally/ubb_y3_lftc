import os
from grammar.grammar import Grammar, Nonterminal, Terminal
from grammar.utils import load_grammar


if __name__ == '__main__':
    # grammar_path = os.path.join(
    #     os.getcwd(), 'lab9', 'grammars', 'mlp.grammar.in')
    grammar_path = os.path.join(
        os.getcwd(), 'lab9', 'grammars', 'first-test.in')
    grammar = load_grammar(grammar_path)
    print(repr(grammar))
    print()
    print()
    print(grammar.first)
    print()
    print()
    print(grammar.follow)
    menu = "\n\n1. Production rules by LHS Nonterminal.\n2. Production rules by RHS Nonterminal.\n3. Production rules by RHS Terminal.\n>> "
    newline = '\n'
    while True:
        line = input(menu)
        if not line:
            break

        command = int(line)
        symbol = input("Enter query symbol.\n>> ").strip().rstrip()
        production_rules = []
        if command == 1:
            if not Nonterminal.is_nonterminal(symbol):
                break

            nonterminal = Nonterminal(symbol)
            production_rules = grammar.get_production_rules_by_lhs_nonterminal(
                nonterminal)
        elif command == 2:
            if not Nonterminal.is_nonterminal(symbol):
                break

            nonterminal = Nonterminal(symbol)
            production_rules = grammar.get_production_rules_by_rhs_nonterminal(
                nonterminal)
        elif command == 3:
            if not Terminal.is_terminal(symbol):
                break

            terminal = Terminal(symbol)
            production_rules = grammar.get_production_rules_by_rhs_terminal(
                terminal)

        print(f'Found {len(production_rules)}')
        print(
            f"{newline.join([repr(production_rule) for production_rule in production_rules])}")
