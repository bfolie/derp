import itertools


class VersionNumber:
    """Representation of software version number.

    Parameters
    ----------
    version: str
        A string of the version, e.g., "1.2.3".

    Attributes
    ----------
    version_numbers: List[int]
        Sequence of version numbers, in descending importance

    """

    def __init__(self, version: str):
        self.version = version
        version_strings = version.split('.')
        try:
            version_numbers = [int(x) for x in version_strings]
        except ValueError:
            raise ValueError(f"version {version} is not parseable as a sequence of integers")
        self.version_numbers = version_numbers

    def __eq__(self, other):
        for self_num, other_num in \
                itertools.zip_longest(self.version_numbers, other.version_numbers, fillvalue=0):
            if self_num != other_num:
                return False
        return True

    def __lt__(self, other):
        for self_num, other_num in \
                itertools.zip_longest(self.version_numbers, other.version_numbers, fillvalue=0):
            if self_num < other_num:
                return True
            elif self_num > other_num:
                return False
            else:
                pass
        # Version numbers are equal
        return False

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other
