import os
import numpy as np
import utils
import rules


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
        # CHECK FOR ID
        id_r = rules.Id(self.__add_id)

        # CHECK FOR CONST
        const_r = rules.Const(self.__add_const)

        # CHECK FOR TYPE
        type_r = rules.Type(self.__types)

        # CHECK FOR DECLARATION
        declaration_r = rules.Declaration(id_r, type_r)

        # CHECK FOR PARAM
        param_r = rules.Param(declaration_r)

        # CHECK FOR READ STATEMENT
        read_r = rules.Read(
            id_r, declaration_r, self.__operators['assignment'])

        # CHECK FOR WRITE STATEMENT
        write_r = rules.Write(id_r, const_r)

        # CHECK FOR CONDITION
        condition_r = rules.Condition(
            id_r, const_r, self.__operators['equality'])

        # CHECK FOR COMPOUND CONDITION
        compound_condition_r = rules.CompoundCondition(
            condition_r, self.__operators['logical'])

        # CHECK FOR IF STATEMENT
        if_r = rules.If(compound_condition_r)

        # CHECK FOR WHILE STATEMENT
        while_r = rules.While(compound_condition_r)

        # CHECK FOR OPERATION
        operation_r = rules.Operation(
            id_r, const_r, self.__operators['arithmetic'])

        # CHECK FOR ASSIGNMENT
        assignment_r = rules.Assignment(
            id_r, declaration_r, operation_r, self.__operators['assignment'])

        # CHECKS FOR TRAILING }
        statement_ending_r = rules.StatementEnding()

        # Add all Rules
        self.__rules = [
            param_r,
            read_r,
            write_r,
            if_r,
            while_r,
            assignment_r,
            operation_r,
            statement_ending_r]

    def analyze(self, source_code) -> [utils.Atom]:
        self.__ids = []
        self.__consts = []

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
                            if int(key) in self.__consts:
                                val = 'CONST'
                        except:
                            val = key

                    atoms.append(utils.Atom(key, self.__atoms[val]))

        return atoms, np.unique(np.array(self.__ids[:])).tolist(), np.unique(np.array(self.__consts[:])).tolist()
