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


class MutableString:
    """
        This class is a wrapper over a string value.
    """

    def __init__(self, value=''):
        self.__value = value

    def strip(self, start=0, end=None):
        """
        Strips all contiguous spaces.

        Args:
            start (int, optional): Starting point. Defaults to 0.
            end (int, optional): Ending point. Defaults to None.
        """
        if not end:
            end = len(self.__value)

        while start < end and self.__value[start] == ' ':
            left = self.__value[:start]
            right = ''
            if start + 1 < end:
                right = self.__value[start + 1:]
            self.__value = left + right

    def __call__(self, value=None):
        """Get or set the value

        Returns:
            value: the value
        """

        if value:
            self.__value = value

        return self.__value


class Atom:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{str(self.value).rjust(4)} : {self.key}"
