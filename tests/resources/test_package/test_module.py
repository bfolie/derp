"""A dummy module for testing the application"""
from deprecation import deprecated


@deprecated(deprecated_in="0.12.3", removed_in="1.0.0")
class OlderDeprecatedClass:

    def __init__(self, name: str):
        self.name = name


@deprecated(deprecated_in="1.2.3", removed_in="2.0.0")
class NewerDeprecatedClass:

    def __init__(self, name1: str, name2: str):
        self.name1 = name1
        self.name2 = name2


class LiveClass:

    def __init(self, x: int):
        self.x = x

    def square(self):
        return self.x ** 2

    @deprecated(deprecated_in="0.1.2.3.4", removed_in="1.0.x")
    def cube(self):
        return self.x ** 3

    @deprecated()
    def quartic(self):
        return self.x ** 4

    def display(self):

        @deprecated(deprecated_in="0.4", removed_in="0.99")
        def _old_display(i: int):
            print(i)

        def _new_display(i: int):
            print(f"{i}!")

        for i in range(self.x):
            _new_display(i)
