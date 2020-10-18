import os
import json
import avl
import rules
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
    source_code_path = os.path.join(os.getcwd(), "lab1\\4_analyser\\sources")
    output_path = os.path.join(os.getcwd(), "lab1\\4_analyser\\outputs")
    config_path = os.path.join(
        os.getcwd(), "lab1\\4_analyser\\powershell.json")
    atoms, types, operators, pairs = load_config(config_path)

    lexer = analyser.PowerShellAnalyser(atoms, types, operators, pairs)

    for file_index, file in enumerate(os.listdir(source_code_path)):
        file_input_path = os.path.join(source_code_path, file)
        if os.path.isfile(file_input_path):
            print(f"====== OUTPUT {str(file_index + 1)} ======")
            source_code = load_source_code(file_input_path)
            atoms, ids, consts = lexer.analyze(source_code)
            ids_tree = avl.AVLTree()
            for id in ids:
                ids_tree.insert(id)

            consts_tree = avl.AVLTree()
            for const in consts:
                consts_tree.insert(const)

            file_output_path = os.path.join(output_path, file)
            with open(file_output_path, 'w') as fout:
                print("=== IDS ===")
                fout.write("=== IDS ===" + os.linesep)

                ids_tree_in = ids_tree.inorder()
                print(ids_tree_in)
                fout.write(str(ids_tree_in))
                fout.write(os.linesep)

                print("=== CONSTS ===")
                fout.write("=== CONSTS ===" + os.linesep)

                consts_tree_in = consts_tree.inorder()
                print(consts_tree_in)
                fout.write(str(consts_tree_in))
                fout.write(os.linesep)

                print("=== ATOMS ===")
                fout.write("=== ATOMS ===" + os.linesep)
                for atom in atoms:
                    print(atom)
                    fout.write(str(atom) + os.linesep)
