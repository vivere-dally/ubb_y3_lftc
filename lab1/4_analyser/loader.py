import abc


class Loader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self, path: str):
        pass


class PowerShellAtomsLoader(Loader):
    def load(self, path: str):
        """Loads the PowerShell lexical atoms and their codes from a config file.

        Args:
            path (str): Path to the config file.

        Returns:
            [dict]: A dictionary that contains the Atoms as keys and their values as values.
        """
        config = {}
        with open(path, 'r') as fin:
            for line in fin:
                line = line.rstrip()
                if not line:
                    continue

                key, val = line.split('~')
                config[key] = int(val)

        return config


class PowerShellTypesLoader(Loader):
    def load(self, path: str):
        """Loads the PowerShell types from a config file.

        Args:
            path (str): Path to the config file.

        Returns:
            [list]: A list that contains the Types.
        """
        types = []
        with open(path, 'r') as fin:
            for line in fin:
                line = line.rstrip()
                if not line:
                    continue

                types.append(line)

        return types


class PowerShellPairsLoader(Loader):
    def load(self, path: str):
        """Loads the PowerShell pairs from a config file.

        Args:
            path (str): Path to the config file.

        Returns:
            [list]: A 2D list that contains the Pairs. 
                    list[i][0] - left pair.
                    list[i][1] - right pair.
        """
        pairs = []
        with open(path, 'r') as fin:
            for line in fin:
                line = line.rstrip()
                if not line:
                    continue

                left, right = line.split('~')
                pairs.append([left, right])

        return pairs
