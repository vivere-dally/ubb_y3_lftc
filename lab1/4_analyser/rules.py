from typing import Callable
import os
import utils
import analyser


class Id(utils.Rule):
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


class Const(utils.Rule):
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


class Type(utils.Rule):
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
