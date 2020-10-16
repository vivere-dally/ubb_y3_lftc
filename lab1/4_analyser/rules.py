from typing import Callable
import abc
import os
import utils
import analyser


class Rule(metaclass=abc.ABCMeta):
    def _strip_until(self, line: str, start: utils.MutableInt) -> None:
        """Removes unnecessary spaces

        Args:
            line (str): The line that will be processed.
            start (utils.MutableInt): The index specifying where to start searching.
        """
        while line[start()] == ' ':
            left = line[:start()]
            if start() + 1 < len(line):
                right = line[start() + 1:]
            line = left + right

    @abc.abstractmethod
    def check(self, line: str, start: utils.MutableInt) -> []:
        """
        Checks if this rule applies
        By default, this method checks if the start parameter got to the end of line.

        Args:
            line (str): The current line that is getting checked.
            start (utils.MutableInt): The starting index where the rule should start checking from.

        Returns:
            []: returns a list with indexes if the rule applies or a rule with -1 if an error is found while checking.
        """

        self._strip_until(line, start)
        return True if len(line) == start() else False


class Id(Rule):
    """
        This class checks the given line from the given index for a PowerShell ID.
    """

    def __init__(self, add_id: Callable, identifier_length=8):
        """
        Args:
            add_id (Callable): Callback that should take a string as parameter. It will get called when a valid ID is found.
            identifier_length (int, optional): The max length of a valid ID. Defaults to 8.
        """
        self.__identifier_length = identifier_length
        self.__add_id = add_id

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Id, self).check(line, start):
            return []

        if line[start()] != "$":
            return []

        result = [start.inc]
        finish = start()
        while finish < len(line):
            if finish - start() < self.__identifier_length:
                if not line[finish].isalnum():
                    break
                else:
                    finish += 1
            else:
                return [-1]

        if start() != finish:
            self.__add_id(line[start():finish])
            result.append(start(finish))

        return result


class Const(Rule):
    """
        This class checks the given line from the given index for a PowerShell Const.
    """

    def __init__(self, add_const: Callable):
        """
        Args:
            add_const (Callable): Callback that should take a string as parameter. It will get called when a valid Const is found.
        """
        self.__add_const = add_const

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Const, self).check(line, start):
            return []

        finish = start()
        while finish < len(line):
            if not line[finish].isdigit():
                break
            else:
                finish += 1

        if start() != finish:
            self.__add_const(line[start():finish])
            return [start(finish)]

        return []


class Type(Rule):
    """
        This class checks the given line from the given index for a PowerShell Type.
    """

    def __init__(self, types: [str]):
        """
        Args:
            types ([str]): List of strings representing the PowerShell Types.
        """
        self.__types = types

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Type, self).check(line, start):
            return []

        finish = start()
        while finish < len(line):
            if not line[finish].isalpha():
                break
            else:
                finish += 1

        if line[start():finish] in self.__types:
            return [start(finish)]

        return []


class Declaration(Rule):
    """
        This class checks the given line from the given index for a PowerShell Declaration.
    """

    def __init__(self, id: Rule, type: Rule):
        """
        Args:
            id (Rule): Rule that checks if a pattern is a PowerShell ID.
            type (Rule): Rule that checks if a pattern is a PowerShell Type.
        """
        self.__id = id
        self.__type = type

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Declaration, self).check(line, start):
            return []

        if line[start()] != '[':
            return []

        self._strip_until(line, start)  # CASE: [    <TYPE>]
        results = [start(), start.inc]
        results.extend(self.__type.check(line, start))
        self._strip_until(line, start)  # CASE: [    <TYPE>    ]
        if line[start()] != ']':
            return [-1]

        self._strip_until(line, start)  # CASE: [    <TYPE>    ]    $ID
        results.extend([start(), start.inc])
        results.extend(self.__id.check(line, start))
        return results


class DeclarationList(Rule):
    """
        This class checks the given line from the given index for PowerShell Declarations.
    """

    def __init__(self, declaration: Rule):
        """
        Args:
            declaration (Rule): Rule that checks if a pattern is a PowerShell Declaration.
        """
        self.__declaration = declaration

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(DeclarationList, self).check(line, start):
            return []

        results = []
        finish = 0
        while finish < len(line) and finish != start():
            finish = start()
            results.extend(self.__declaration.check(line, start))
            self._strip_until(line, start)  # CASE: <DECLARATION>    ;
            if start() == finish or line[start()] != ';':
                return results
            else:
                results.extend([start(), start.inc])

        return results


class Param(Rule):
    """
        This class checks the given line from the given index for PowerShell Param.
    """

    def __init__(self, declaration: Rule):
        """
        Args:
            declaration (Rule): Rule that checks if a pattern is a PowerShell Declaration.
        """
        self.__declaration = declaration

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        if line[start():start() + 5] != "param":
            return []

        results = [start(), start(start() + 5)]
        self._strip_until(line, start)  # CASE: param    (
        if line[start()] != '(':
            return [-1]

        results.extend([start(), start.inc])
        finish = 0
        while finish < len(line) and finish != start():
            finish = start()
            results.extend(self.__declaration.check(line, start))
            self._strip_until(line, start)  # CASE: <DECLARATION>    ,
            if start() == finish or line[start()] != ',':
                return results
            else:
                results.extend([start(), start.inc])

        self._strip_until(line, start)  # CASE: <DECLARATION>    )
        if line[start()] != ')':
            return [-1]

        results.extend([start(), start.inc])
        return results
