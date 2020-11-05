import os
import json
from fa.finite_automaton import load_fa_from_file
from analyser.analyser import Analyser
from analyser.avl import AVLTree


def load_fas(path):
    fas = []
    for file_index, file in enumerate(os.listdir(path)):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            fas.append(load_fa_from_file(file_path))

    return fas


def load_config(path):
    atoms = {}
    with open(path) as fin:
        data = json.load(fin)
        for atom in data['atoms']:
            atoms[atom['key']] = atom['value']

    return atoms


def load_source_code(path):
    source_code = None
    with open(path) as fin:
        source_code = fin.readlines()

    return source_code


def get_inorder(X: list) -> list:
    tree = AVLTree()
    for x in X:
        tree.insert(x)

    return tree.inorder()


def write_to_file(path, writable, mode='w'):
    with open(path, mode) as fout:
        fout.write(writable)
        fout.flush()


if __name__ == '__main__':
    # Paths
    fa_dir_path = os.path.join(os.getcwd(), "lab4\\fa\\fas")
    config_path = os.path.join(os.getcwd(), "lab4\\analyser\\powershell.json")
    source_code_dir_in = os.path.join(os.getcwd(), "lab4\\analyser\\in")
    source_code_dir_out = os.path.join(os.getcwd(), "lab4\\analyser\\out")

    # Prep
    fas = load_fas(fa_dir_path)
    atoms = load_config(config_path)
    lexer = Analyser(atoms, fas)

    # Work
    for file in os.listdir(source_code_dir_in):
        fin = os.path.join(source_code_dir_in, file)
        fout = os.path.join(source_code_dir_out, file)
        atoms, ids, consts, string_consts = lexer.analyze(
            load_source_code(fin))

        write_to_file(fout, f"IDS: {get_inorder(ids)}\n\n", 'w')
        write_to_file(fout, f"CONSTS: {get_inorder(consts)}\n\n", 'a')
        write_to_file(
            fout, f"STRING_CONSTS: {get_inorder(string_consts)}\n\n", 'a')
        writable = "\n".join([str(atom) for atom in atoms])
        write_to_file(fout, f"ATOMS:\n{writable}\n\n", 'a')
