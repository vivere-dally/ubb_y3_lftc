import os

from typing import List

from lab9.grammar.symbols.terminal import Terminal

PS_LEXER_PATH = os.path.join('lab5', 'pslexer.exe')


def extract_atoms(file_in_path: str, file_out_path: str) -> List[Terminal]:
    cwd_parent = os.path.abspath(os.path.join(os.getcwd(), '../.'))
    exe_path = os.path.join(cwd_parent, PS_LEXER_PATH)
    os.system(f"{exe_path} < {file_in_path} > {file_out_path}")
    buffer = []
    with open(file_out_path, 'r') as f_out:
        for line in f_out:
            line = line.strip().rstrip()
            if not line:
                break

            tokens = [token.strip() for token in line.split(':')]
            id = int(tokens[1].strip())  # Useless now?
            terminal = None
            if tokens[0] == 'ID':
                terminal = Terminal('id')
            elif tokens[0] == 'CONST':
                terminal = Terminal('constant')
            elif tokens[0] == 'STR CONST':
                terminal = Terminal('string_constant')
            else:
                terminal = Terminal(tokens[2].strip())

            buffer.append(terminal)

    return buffer
