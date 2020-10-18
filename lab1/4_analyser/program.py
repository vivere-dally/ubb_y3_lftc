import os
import json
import rules
import loader
import analyser


def load_source_code(path):
    source_code = None
    with open(path) as fin:
        source_code = fin.readlines()

    return source_code


def load_config(path):
    atoms = {}
    types = None
    operators = {}
    pairs = []
    with open(path) as fin:
        data = json.load(fin)
        for atom in data['atoms']:
            atoms[atom['key']] = atom['value']

        types = data['types']
        for key, value in data['operators'].items():
            operators[key] = value

        pairs = data['pairs']

    return atoms, types, operators, pairs


if __name__ == "__main__":
    source_code_path = os.path.join(
        os.getcwd(), "lab1\\4_analyser\\source.txt")
    source_code = load_source_code(source_code_path)
    config_path = os.path.join(
        os.getcwd(), "lab1\\4_analyser\\powershell.json")
    atoms, types, operators, pairs = load_config(config_path)

    lexer = analyser.PowerShellAnalyser(atoms, types, operators, pairs)
    atoms = lexer.analyze(source_code)

    for atom in atoms:
        print(f"{str(atom.value).rjust(4)} : {atom.key}")
