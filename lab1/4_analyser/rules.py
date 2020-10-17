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


class Read(Rule):
    """
        This class checks the given line from the given index for PowerShell Read-Host.
    """

    def __init__(self, id: Rule, declaration: Rule):
        """
        Args:
            id (Rule): Rule that checks if a pattern is a PowerShell ID.
            declaration (Rule): Rule that checks if a pattern is a PowerShell Declaration.
        """
        self.__id = id
        self.__declaration = declaration

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        results = self.__declaration.check(line, start)
        if 0 == len(results):
            results = self.__id.check(line, start)
            if 0 == len(results):
                return []

        self._strip_until(line, start)  # CASE: <DECLARATION> | <ID>    =
        if '=' != line[start()]:
            return results

        results.extend([start(), start.inc])
        self._strip_until(line, start)  # CASE: ...    Read-Host
        if "Read-Host" != line[start(): start() + 9]:
            return results

        results.extend([start(), start(start() + 9)])
        self._strip_until(line, start)  # CASE: Read-Host     ;
        if ';' == line[start()]:
            results.append([start(), start.inc])
            return results

        return results


class Write(Rule):
    """
        This class checks the given line from the given index for PowerShell Write-Host.
    """

    def __init__(self, id: Rule, const: Rule):
        """
        Args:
            id (Rule): Rule that checks if a pattern is a PowerShell ID.
            const (Rule): Rule that checks if a pattern is a PowerShell Const.
        """
        self.__id = id
        self.__const = const

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        results = []
        if "Write-Host " != line[start(): start() + 11]:
            return []

        results.extend([start(), start(start() + 11)])
        self._strip_until(line, start)  # CASE: Write-Host     <ID>
        results_ = self.__id.check(line, start)
        if 0 == len(results_):
            results_ = self.__const.check(line, start)
            if 0 == len(results_):
                start.inc
                results.append(-1)
                return results

        self._strip_until(line, start)  # CASE: Write-Host <ID>    ;
        if ';' == line[start()]:
            results.append([start(), start.inc])
            return results

        return results


class Condition(Rule):
    """
        This class checks the given line from the given index for PowerShell Condition.
    """

    def __init__(self, id: Rule, const: Rule, equality_operators: List):
        """
        Args:
            id (Rule): Rule that checks if a pattern is a PowerShell ID.
            const (Rule): Rule that checks if a pattern is a PowerShell Const.
            equality_operators (List): List of PowerShell equality operators.
        """
        self.__id = id
        self.__const = const
        self.__equality_operators = equality_operators

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        results = self.__id.check(line, start)
        if 0 == len(results):
            results = self.__const.check(line, start)
            if 0 == len(results):
                return []

        self._strip_until(line, start)  # CASE: ID | CONST    <EQ_OP>
        eq_op_found = False
        for eq_op in self.__equality_operators:
            if eq_op_found:
                break

            if eq_op == line[start(), start() + len(eq_op)]:
                eq_op_found = True
                results.extend([start(), start(start() + len(eq_op))])

        if not eq_op_found:
            return results

        self._strip_until(line, start)  # CASE: <EQ_OP>    ID | CONST
        results_ = self.__id.check(line, start)
        if 0 == len(id):
            results_ = self.__const.check(line, start)
            if 0 == len(results_):
                start.inc
                results.add(-1)
                return results

        results.extend(results_)
        return results


class CompoundCondition(Rule):
    """
        This class checks the given line from the given index for PowerShell Compound Condition.
    """

    def __init__(self, condition: Rule, logical_operators: List):
        """
        Args:
            condition (Rule): Rule that checks if a pattern is a PowerShell Condition.
            logical_operators (List): List of PowerShell logical operators.
        """
        self.__id = id
        self.__condition = condition
        self.__logical_operators = logical_operators

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        results = []
        if '(' == line[start(), start() + 1]:
            start.inc
            results.extend(self.check(line, start))

        self._strip_until(line, start)  # CASE: (    <CONDITION>
        results.extend(self.__condition.check(line, start))
        self._strip_until(line, start)  # CASE: <CONDITION>    )
        while ')' == line[start(), start() + 1]:
            results.extend([start(), start.inc])
            self._strip_until(line, start)  # CASE: <CONDITION>    )    )

        self._strip_until(line, start)  # CASE: )    <LG_OP>
        lg_op_found = False
        for lg_op in self.__logical_operators:
            if lg_op_found:
                break

            if lg_op == line[start(), start() + len(lg_op)]:
                lg_op_found = True
                results.extend([start(), start(start() + len(lg_op))])

        if not lg_op_found:
            return results

        self._strip_until(line, start)  # CASE: <LG_OP>    (
        if '(' == line[start(), start() + 1]:
            start.inc
            results.extend(self.check(line, start))

        return results


class If(Rule):
    """
        This class checks the given line from the given index for PowerShell if statement.
    """

    def __init__(self, compoundCondition: Rule):
        """
        Args:
            compoundCondition (Rule): Rule that checks if a pattern is a PowerShell Compound Condition.
        """
        self.__id = id
        self.__compoundCondition = compoundCondition

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        if "if" != line[start(), start() + 2]:
            return []

        results = [start(), start(start() + 2)]
        self._strip_until(line, start)  # CASE: if    (
        if '(' != line[start(), start() + 1]:
            start.inc
            results.append(-1)
            return results

        results.extend(self.__compoundCondition.check(line, start))
        self._strip_until(line, start)  # CASE: <CP_CON>   )
        if ')' == line[start(), start() + 1]:
            results.extend([start(), start.inc])

        self._strip_until(line, start)  # CASE: )    {
        if '{' != line[start(), start() + 1]:
            start.inc
            results.append(-1)
            return results

        results.extend([start(), start.inc])
        return results


class While(Rule):
    """
        This class checks the given line from the given index for PowerShell while statement.
    """

    def __init__(self, compoundCondition: Rule):
        """
        Args:
            compoundCondition (Rule): Rule that checks if a pattern is a PowerShell Compound Condition.
        """
        self.__id = id
        self.__compoundCondition = compoundCondition

    def check(self, line: str, start: utils.MutableInt) -> []:
        if super(Param, self).check(line, start):
            return []

        if "while" != line[start(), start() + 5]:
            return []

        results = [start(), start(start() + 2)]
        self._strip_until(line, start)  # CASE: while    (
        if '(' != line[start(), start() + 1]:
            start.inc
            results.append(-1)
            return results

        results.extend(self.__compoundCondition.check(line, start))
        self._strip_until(line, start)  # CASE: <CP_CON>   )
        if ')' == line[start(), start() + 1]:
            results.extend([start(), start.inc])

        self._strip_until(line, start)  # CASE: )    {
        if '{' != line[start(), start() + 1]:
            start.inc
            results.append(-1)
            return results

        results.extend([start(), start.inc])
        return results
