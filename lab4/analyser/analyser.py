from fa.finite_automaton import FiniteAutomaton
from analyser.errors import UnexpectedTokenError
import numpy as np


class Atom:
    def __init__(self, token, key, value):
        self.token = token
        self.key = key
        self.value = value

    def __repr__(self):
        return f"{str(self.value).rjust(2)} : {self.key}"


class Analyser:
    """
        Class used for lexical analysis of a PowerShell file.
    """

    def __init__(self, atoms: dict, fas: list):
        """
            Initialize Analyser.

        Args:
            atoms (dict<str, str>): Key = lexical atom, value = id
            fas (list<FiniteAutomaton>): list of defined finite automatons
        """
        self.__atoms = atoms
        self.__fas = fas

    def __refresh(self):
        self.__found_atoms = []
        self.__found_ids = []
        self.__found_constants = []
        self.__found_string_constants = []

    def __add_token(self, atom: Atom):
        if atom.key == "ID":
            self.__found_ids.append(atom)
        elif atom.key == "CONST":
            self.__found_constants.append(atom)
        elif atom.key == "STRING_CONST":
            self.__found_string_constants.append(atom)
        else:
            self.__found_atoms.append(atom)

    def analyze(self, source_code: list) -> (list, list, list, list):
        """[summary]

        Args:
            self ([type]): [description]
            list ([type]): [description]
            list ([type]): [description]
            list ([type]): [description]

        Raises:
            UnexpectedTokenError: [description]

        Returns:
            [type]: [description]
        """
        self.__refresh()
        for line_index, line in enumerate(source_code):
            line = line.strip().rstrip()
            if not line:
                continue

            prev = 0
            curr = 0
            check_fas = True
            while curr < len(line):
                curr += 1
                atom = None
                line_part = line[prev:curr]
                if check_fas:
                    found = False
                    line_rest = line[prev:]
                    for fa in self.__fas:
                        prefix = fa.get_longest_prefix(line_rest)
                        if prefix:
                            # ID OR CONST
                            if fa.atom in self.__atoms:
                                atom = Atom(prefix, fa.atom,
                                            self.__atoms[fa.atom])
                            # OPERATOR
                            else:
                                atom = Atom(fa.atom, prefix,
                                            self.__atoms[prefix])

                            found = True
                            prev += len(prefix)
                            curr = prev
                            break

                    # Stop checking the Finite Automatons because there are unexpected characters at the beginning.
                    check_fas = found

                # If check_fas is True, it means we found an accepted sequence by one of the fas.
                if line_part in self.__atoms and not check_fas:
                    atom = Atom(line_part, line_part, self.__atoms[line_part])
                    prev = curr
                    check_fas = True

                if atom:
                    self.__add_token(atom)

            if prev != curr:
                raise UnexpectedTokenError(
                    line_index + 1, prev + 1, line[prev])

        # Get only the unique values
        self.__found_ids = np.unique(
            np.array([atom.token for atom in self.__found_ids]))
        self.__found_constants = np.unique(
            np.array([atom.token for atom in self.__found_constants]))
        self.__found_string_constants = np.unique(
            np.array([atom.token for atom in self.__found_string_constants]))
        return self.__found_atoms, self.__found_ids, self.__found_constants, self.__found_string_constants
