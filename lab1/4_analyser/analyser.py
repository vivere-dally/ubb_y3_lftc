import os
import utils
import rules
import loader


class PowerShellAnalyser:
    """
        Class used for analyzing a PowerShell code file 
    """

    class PowerShellPreprocessor:
        def __init__(self, pairs: []):
            self.__pairs = pairs

        def process(self, source_code):
            for pair in self.__pairs:
                a = []
                for line_index, line in enumerate(source_code):
                    for char_index, char in enumerate(line):
                        if char == pair['opening']:
                            a.append([line_index + 1, char_index + 1])
                        elif char == pair['closing']:
                            try:
                                a.pop()
                            except:
                                print(
                                    f"Found '{pair['closing']}' on line {str(line_index + 1)} character {str(char_index + 1)}. Missing opening '{pair['opening']}'...")

                if 0 != len(a):
                    for a_ in a:
                        print(
                            f"Found '{pair['opening']}' on line {str(a_[0])} character {str(a_[1])}. Missing closing '{pair['closing']}'...")

    def __init__(self, atoms, types, operators, pairs, identifier_length=8):
        self.__atoms = atoms
        self.__types = types
        self.__operators = operators
        self.__pairs = pairs
        self.__identifier_length = identifier_length

        self.__ids = []
        self.__consts = []
        self.__rules = []

        self.__init_rules()

    def __add_id(self, id: str):
        self.__ids.append(id)

    def __add_const(self, const):
        self.__consts.append(int(const))

    def __init_rules(self):
        id_r = rules.Id(self.__add_id)
        const_r = rules.Const(self.__add_const)
        type_r = rules.Type(self.__types)
        declaration_r = rules.Declaration(id_r, type_r)
        declaration_list_r = rules.DeclarationList(declaration_r)
        param_r = rules.Param(declaration_r)
        read_r = rules.Read(id_r, declaration_r)
        write_r = rules.Write(id_r, const_r)
        condition_r = rules.Condition(
            id_r, const_r, self.__operators['equality'])
        compound_condition_r = rules.CompoundCondition(
            condition_r, self.__operators['logical'])
        if_r = rules.If(compound_condition_r)
        while_r = rules.While(compound_condition_r)
        self.__rules = [param_r, read_r, write_r, if_r,
                        while_r, declaration_list_r, declaration_r]

    def analyze(self, source_code) -> [utils.Atom]:
        psp = self.PowerShellPreprocessor(self.__pairs)
        psp.process(source_code)

        atoms: [utils.Atom] = []
        for line_index, line in enumerate(source_code):
            line = line.rstrip()
            line = line.strip()
            if not line:
                continue

            line = utils.MutableString(line)
            start = utils.MutableInt()
            patterns = [start()]
            while start() < len(line()):
                if -1 in patterns:
                    break

                beginning = start()
                for rule in self.__rules:
                    patterns.extend(rule.check(line, start))

                if beginning == start():
                    patterns.append(-1)

            for i in range(1, len(patterns)):
                if patterns[i] == -1:
                    token = None
                    try:
                        token = line()[patterns[i - 1] + 1]
                    except:
                        token = line()[patterns[i - 1]]
                    print(
                        f"Error on line {str(line_index + 1)} character {str(patterns[i - 1] + 1)}. Token: '{token}'")
                else:
                    key = line()[patterns[i - 1]: patterns[i]]
                    val = None
                    if key in self.__ids:
                        val = 'ID'
                    else:
                        try:
                            if int(key) in self.__const:
                                val = 'CONST'
                        except:
                            val = key

                    atoms.append(utils.Atom(key, self.__atoms[val]))

        self.__ids = []
        self.__consts = []
        return atoms


if __name__ == "__main__":
    psa = loader.PowerShellAtomsLoader()
    atoms = psa.load(os.path.join(
        os.getcwd(), "lab1\\4_analyser\\configs\\PowerShellAtoms.config"))

    psp = loader.PowerShellPairsLoader()
    pairs = psp.load(os.path.join(
        os.getcwd(), "lab1\\4_analyser\\configs\\PowerShellPairs.config"))

    pst = loader.PowerShellTypesLoader()
    types = pst.load(os.path.join(
        os.getcwd(), "lab1\\4_analyser\\configs\\PowerShellTypes.config"))

    source_code = None
    with open(os.path.join(os.getcwd(), "lab1\\4_analyser\\source.txt"), "r") as fin:
        source_code = fin.readlines()

    lexer = PowerShellAnalyser(atoms, pairs, types)
    atoms = lexer.analyze(source_code)
    for atom in atoms:
        print(f"{str(atom.value).rjust(4)} : {atom.key}")
