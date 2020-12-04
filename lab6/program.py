import os
from grammar import Grammar

BUDGET_EPSILON = '#'


def load_grammar(path: str) -> Grammar:
    nonterminals = set()
    terminals = set()
    production_rules = {}
    with open(path) as fin:
        for line in fin:
            lhs, rhs = line.strip().rstrip().split('->')
            for symbol in lhs:
                nonterminals.add(symbol)
            
            for symbol in rhs:
                if symbol not in nonterminals:
                    terminals.add(symbol)

            if lhs in production_rules:
                production_rules[lhs].append(rhs)
            else:
                production_rules[lhs] = [rhs]

    nonterminals = ''.join(nonterminals)
    terminals = ''.join(terminals)
    return Grammar(nonterminals, terminals, production_rules)


if __name__ == '__main__':
    grammar_path = os.path.join(os.getcwd(), 'lab6', 'grammar.in')
    grammar = load_grammar(grammar_path)
    while True:
        nonterminal = input('Enter a nonterminal > ')
        if not nonterminal:
            break

        production_rules = grammar.get_production_rules_by_nonterminal(
            nonterminal)
        print(f'Found {len(production_rules)} production rules')
        for production_rule in production_rules:
            print(production_rule)

        print()
