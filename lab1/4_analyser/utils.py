import abc


class MutableInt:
    """
        This class is a wrapper over an integer value.
    """

    def __init__(self, value=0):
        self.__value = value

    @property
    def inc(self):
        """Add 1 to value

        Returns:
            int: the value
        """

        self.__value += 1
        return self.__value

    @property
    def dec(self):
        """Subtract 1 from value

        Returns:
            int: the value
        """

        self.__value -= 1
        return self.__value

    def __call__(self, value=None):
        """Get or set the value

        Returns:
            int: the int
        """

        if value:
            self.__value = value

        return self.__value


class Rule(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def check(self, line: str, start: MutableInt) -> []:
        """
        Checks if this rule applies
        By default, this method checks if the start parameter got to the end of line.

        Args:
            line (str): The current line that is getting checked.
            start (MutableInt): The starting index where the rule should start checking from.

        Returns:
            []: returns a list with indexes if the rule applies or a rule with -1 if an error is found while checking.
        """
        return True if len(line) == start() else False


class Atom:
    def __init__(self, key, value):
        self.key = key
        self.value = value
