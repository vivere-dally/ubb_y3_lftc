import os
import utils
import rules
import loader


class Atom:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class OldAnalyser:
    def __init__(self, config, identifier_length=8, combined=True):
        self.__ids = []
        self.__constants = []
        self.__all = []
        self.__config = config
        self.__identifier_length = 8
        self.__combined = True
        self.__reset(None)

    def __reset(self, source_code):
        self.__source_code = source_code
        self.__atoms = []

    def __is_end_line(self, line, start):
        if start.value == len(line):
            return True

        return False

    def __add_id_const(self, value, is_id=True):
        if self.__combined:
            self.__all.append(value)
        elif is_id:
            self.__ids.append(value)
        else:
            self.__constants.append(int(value))

    def __get_id_const(self, value):
        if self.__combined:
            if value in self.__all:
                try:
                    value_as_int = int(value)
                    return "CONST"
                except ValueError:
                    return "ID"
        else:
            if value in self.__ids:
                return "ID"
            try:
                value_as_int = int(value)
                if value_as_int in self.__constants:
                    return "CONST"
            except ValueError:
                return None

        return None

    def __is_id(self, line, start):
        if self.__is_end_line(line, start):
            return []

        if line[start.value] != "$":
            return []

        result = [start.inc]
        finish = start.value
        while finish < len(line):
            if finish - start.value < self.__identifier_length:
                if not line[finish].isalnum():
                    break
                else:
                    finish += 1
            else:
                return [-1]

        if start.value != finish:
            self.__add_id_const(line[start.value:finish])
            start.value = finish
            result.append(finish)

        return result

    def __is_const(self, line, start):
        if self.__is_end_line(line, start):
            return []

        finish = start.value
        while finish < len(line):
            if not line[finish].isdigit():
                break
            else:
                finish += 1

        if start.value != finish:
            self.__add_id_const(line[start:finish], is_id=False)
            start.value = finish
            return [finish]

        return []

    def __is_string(self, line, start):
        if self.__is_end_line(line, start):
            return []

        if line[start.value] != '"':
            return []

        result = [start.value, start.inc]
        finish = start.value
        while finish < len(line):
            if line[finish] == '"':  # isalnum for now. Change to any character until you meet '"'
                break
            elif not line[finish].isalnum():
                break
            else:
                finish += 1

        if start.value == finish or finish == len(line):  # no closing '"'
            return [-1]

        start.value = finish
        result.append(start.value)
        result.append(start.inc)
        return result

    def __is_declaration(self, line, start):
        if self.__is_end_line(line, start):
            return []

        if line[start.value] != '[':
            return []

        results = [start.value, start.inc]
        results.extend(self.__is_type(line, start))
        if line[start.value] != ']':  # ERROR Did not find closing ']'
            return [-1]

        results.extend([start.value, start.inc])
        results.extend(self.__is_id(line, start))
        return results

    def __is_param(self, line, start):
        pass

    def __is_separator(self, line, start, specific_separator=None):
        if self.__is_end_line(line, start):
            return []

        separators = ["(", ")", "[", "]", "{", "}", ",", ";", " "] if not specific_separator else [
            specific_separator]
        if line[start.value] in separators:
            start.value += 1
            return [start.value]

        return []

    def __is_keyword(self, line, start, specific_keyword=None):
        if self.__is_end_line(line, start):
            return []

        keywords = ["param", "Read-Host",
                    "Write-Host"] if not specific_keyword else [specific_keyword]
        for keyword in keywords:
            finish = line.find(keyword, start.value)
            if finish != -1:
                finish += len(keyword)
                start.value = finish
                return [finish]

        return []

    def __is_type(self, line, start, specific_type=None):
        if self.__is_end_line(line, start):
            return []

        finish = start.value
        while finish < len(line):
            if not line[finish].isalpha():
                break
            else:
                finish += 1

        types = ["int", "string", "bool",
                 "array"] if not specific_type else [specific_type]
        if line[start.value: finish] in types:
            start.value = finish
            return [finish]

        return []

    def __is_comparison(self, line, start):
        if self.__is_end_line(line, start):
            return []

        comparisons = ["-lt", "-le", "-eq", "-ne",
                       "-gt", "-ge", "-and", "-or", "-not"]
        if line[start.value: start.value + 3] in comparisons:
            start.value += 3
            return [start.value]

        return []

    def __is_condition(self, line, start):
        return []

    def __is_statement(self, line, start):
        return []

    def __is_operation(self, line, start):
        return []

    def __is_function(self, line, start):
        return []

    def extract(self, source_code):
        self.__reset(source_code)

        for line_index, line in enumerate(source_code):
            line = line.rstrip()
            if not line:
                continue

            start = MutableInt(0)
            indexes = [start.value]
            while start.value < len(line):
                start_copy = MutableInt(start.value)
                indexes.extend(self.__is_)
                indexes.extend(self.__is_separator(line, start))
                indexes.extend(self.__is_keyword(line, start))
                indexes.extend(self.__is_id(line, start))
                indexes.extend(self.__is_const(line, start))
                indexes.extend(self.__is_type(line, start))
                # indexes.extend(self.__is_declaration(line, start))
                indexes.extend(self.__is_operation(line, start))
                indexes.extend(self.__is_condition(line, start))
                indexes.extend(self.__is_statement(line, start))
                # found error
                if -1 in indexes:
                    break

                # we can't determine the character
                if start.value == start_copy.value:
                    indexes.append(-1)
                    break

            for i in range(1, len(indexes)):
                if indexes[i] == -1:
                    self.__atoms.append(
                        Atom(f"Error on line {line_index + 1} character {start.value + 1}", None))
                else:
                    atom = line[indexes[i - 1]: indexes[i]]
                    atom_as_id_or_const = self.__get_id_const(atom)
                    if not atom_as_id_or_const:
                        self.__atoms.append(Atom(atom, self.__config[atom]))
                    else:
                        self.__atoms.append(
                            Atom(atom, self.__config[atom_as_id_or_const]))

        return self.__atoms[:]


class PowerShellAnalyser:
    """
        Class used for analyzing a PowerShell code file 
    """

    def __init__(self, atoms, pairs, types, identifier_length=8):
        self.__atoms = atoms
        self.__pairs = pairs
        self.__types = types
        self.__identifier_length = identifier_length
        self.__ids = []
        self.__const = []
        self.__init_rules()

    class PowerShellPreprocessor:
        def __init__(self, pairs: []):
            self.__pairs = pairs

        def process(self, source_code):
            for pair in self.__pairs:
                a = []
                for line_index, line in enumerate(source_code):
                    for char_index, char in enumerate(line):
                        if char == pair[0]:
                            a.append([line_index + 1, char_index + 1])
                        elif char == pair[1]:
                            try:
                                a.pop()
                            except:
                                print(
                                    f"Found '{pair[1]}' on line {str(line_index + 1)} character {str(char_index + 1)}. Missing opening '{pair[0]}'...")

                if 0 != len(a):
                    for a_ in a:
                        print(
                            f"Found '{pair[0]}' on line {str(a_[0])} character {str(a_[1])}. Missing closing '{pair[1]}'...")

    def __add_id(self, id: str) -> None:
        self.__ids.append(id)

    def __add_const(self, const: str) -> None:
        self.__const.append(int(const))

    def __init_rules(self):
        self.__rules: [rules.Rule] = []
        self.__rules.append(rules.Id(self.__add_id, self.__identifier_length))
        self.__rules.append(rules.Const(self.__add_const))
        self.__rules.append(rules.Type(self.__types))

    def analyze(self, source_code) -> [utils.Atom]:
        psp = self.PowerShellPreprocessor(self.__pairs)
        psp.process(source_code)

        atoms: [utils.Atom] = []
        for line_index, line in enumerate(source_code):
            line = line.rstrip()
            line = line.strip()
            if not line:
                continue

            start = utils.MutableInt()
            patterns = [start()]
            while start() < len(line):
                if -1 in patterns:
                    break

                beginning = start()
                for rule in self.__rules:
                    rule.check(line, start)

                if beginning == start():
                    patterns.append(-1)

            for i in range(1, len(patterns)):
                if patterns[i] == -1:
                    print(
                        f"Error on line {line_index + 1} character {patterns[i] + 1}. Token: '{line[patterns[i]]}'")
                else:
                    key = line[patterns[i - 1]: patterns[i]]
                    val = None
                    if key in self.__ids:
                        val = 'ID'
                    elif int(key) in self.__const:
                        val = 'CONST'
                    else:
                        val = key

                    atoms.append(Atom(key, self.__atoms[key]))

        self.__ids = []
        self.__const = []
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
