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


class Atom:
    def __init__(self, key, value):
        self.key = key
        self.value = value
