import os


class MutableInt:
    def __init__(self, value):
        self.value = value


class Atom:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Analyser:
    def __init__(self, config, identifier_length=8, combined=True):
        self.__ids = []
        self.__constants = []
        self.__all = []
        self.__config = config
        self.__identifier_length = 8
        self.__combined = True
        self.__reset(None)

# region Private
    def __reset(self, source_code):
        self.__source_code = source_code
        self.__atoms = []

# region Handle ID CONST
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

# endregion

# region Lexical Rules

    def __is_id(self, line, start):
        if self.__is_end_line(line, start):
            return []

        if line[start.value] != "$":
            return []

        start.value += 1
        result = [start.value]
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

# endregion

    def __is_end_line(self, line, start):
        if start.value == len(line):
            return True

        return False

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

# endregion

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


if __name__ == "__main__":
    config_file_path = os.path.join(
        os.getcwd(), "lab1\\4_analyser\\PowerShell.config")
    config = {}
    with open(config_file_path, "r") as fin:
        for line in fin:
            key, val = line.split("~")
            config[key] = int(val)

    source_code_file_path = os.path.join(
        os.getcwd(), "lab1\\4_analyser\\source.txt")
    source_code = None
    with open(source_code_file_path, "r") as fin:
        source_code = fin.readlines()

    lexer = Analyser(config)
    atoms = lexer.extract(source_code)
    for atom in atoms:
        print(f"{str(atom.value).rjust(4)} : {atom.key}")
