import os

from typing import List

from lab9.fip.extract_atoms_ps import extract_atoms
from lab9.grammar.grammar import Grammar
from lab9.grammar.symbols.terminal import Terminal
from lab9.grammar.utils import load_grammar
from lab9.slr.filters import is_left_recursive, is_deterministic
from lab9.slr.first_and_follow import FnF
from lab9.slr.slr import SLR

if __name__ == '__main__':
    result_out = os.path.join(os.getcwd(), 'slr.out')
    grammar_in = os.path.join(os.getcwd(), 'part_3_data', '_.grammar')
    file_in = os.path.join(os.getcwd(), 'part_3_data', '_.in')
    file_out = os.path.join(os.getcwd(), 'part_3_data', '_.out')

    grammar: Grammar = load_grammar(grammar_in)
    print(f"=== GRAMMAR ===\n{repr(grammar)}\n")
    if not is_left_recursive(grammar):
        raise RuntimeError('The given grammar is left recursive!')

    if not is_deterministic(grammar):
        raise RuntimeError('The given grammar is non-deterministic!')

    fnf: FnF = FnF(grammar)
    print(f"=== FIRST&FOLLOW ===\n{repr(fnf)}\n")
    slr = SLR(grammar, fnf)

    buffer: List[Terminal] = extract_atoms(file_in, file_out)
    print(" ".join([repr(item).split(':')[1] for item in buffer]))
    result = slr.parse(buffer)
    with open(result_out, 'w') as out:
        for i in range(len(result), 2):
            print(result[i])
            print(result[i + 1])
            print()
