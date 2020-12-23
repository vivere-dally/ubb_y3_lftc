from itertools import zip_longest

from lab9.grammar.grammar import Grammar


def is_left_recursive(grammar: Grammar) -> bool:
    """
    Check if the given grammar is left recursive. A CFG is left recursive if the first symbol in the right-hand side
    is the same non-terminal as in the left-hand side.
    E.g.:
        1) S->Aa
           A->Ab    <- this production rule is left-recursive

        2) S->Aa
           A->bA
           This grammar is right recursive which is fine in the given context (SLR).
    """

    for pr in grammar.production_rules:
        if pr.lhs == pr.rhs[0]:
            print(f"{pr.lhs} == {pr.rhs[0]}")
            return False

    return True


def is_deterministic(grammar: Grammar) -> bool:
    """
    Checks if the given grammar is deterministic. A CFG is deterministic if for all production rules for a
    non-terminal X the right-hand side is different for all these rules.
    E.g.:
        1) S->abcC
           S->abB
           S->aA
           ...
           This grammar is non-deterministic since when you encounter an 'a' in the text to analyze,
           you have 3 choices to make.

       2) S->cC
          S->bB
          S->aA
          ...
          This grammar is fine.
    """
    for nt in grammar.nonterminals:
        rhss = [pr.rhs for pr in grammar.get_production_rules_by_lhs_nonterminal(nt)]
        for alpha in zip_longest(*rhss, fillvalue=None):
            alpha_l = []
            alpha_s = set()
            for alpha_ in alpha:
                if alpha_ is not None:
                    alpha_l.append(alpha_)
                    alpha_s.add(alpha_)

            if len(alpha_l) != len(alpha_s):
                print(f"{alpha_l} != {alpha_s}")
                return False

    return True
