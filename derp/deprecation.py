"""Classes corresponding to way a developer might mark something as deprecated.
Currently, the only supported option is to use the @deprecated decorator from python's
deprecation library. This is captured with PythonDeprecation. Additional types of deprecation
can be added by creating new classes that extend Deprecation, and including them in the list
``DEPRECATION_TYPE_LIST`` in __init__.py.
"""

import ast
from abc import abstractmethod, ABC
from typing import List, Optional
from derp.version_number import VersionNumber


class Deprecation(ABC):
    """Abstract representation of a way to mark deprecations.
    There are two things any child class ust implement.
    * An initialization method that takes a node of type ast.AST and throws a ValueError
        if it can't be parsed. Deprecations should only be initialized within a
        try-except block.
    * A check_error method that takes the current version and returns a string if there is
        an error, otherwise returns None.
    """

    @abstractmethod
    def check_error(self, current_version: VersionNumber) -> Optional[str]:
        """Return a user-facing error message if the deprecation is invalid."""
        raise NotImplementedError


class PythonDeprecation(Deprecation):
    """Attempt to parse a decorator from python's deprecation package.

    Because we don't know if a node corresponds to a deprecation until we parse it,
    we use exceptions to control the flow of the program.
    ValueErrors are typical when initializing PythonDeprecation, and so it should only
    be initialized within a try-except block.

    Parameters
    ----------
    decorator: ast.AST
        An ast node that is expected to correspond to a decorator

    Raises
    ------
    ValueError
        If the node cannot be parsed as a PythonDeprecation

    """

    def __init__(self, decorator: ast.AST):
        if isinstance(decorator, ast.Call):
            try:
                func: ast.Name = decorator.func
                name: str = func.id
                if not name == "deprecated":
                    raise ValueError("Decorator does not follow Python Deprecation format")
                keyword_dict = dict()
                keywords: List[ast.keyword] = decorator.keywords
                for keyword in keywords:
                    try:
                        arg = keyword.arg
                        value = keyword.value.s
                        keyword_dict[arg] = value
                    except AttributeError:
                        pass
                self.deprecated_in = keyword_dict.get("deprecated_in", None)
                self.removed_in = keyword_dict.get("removed_in", None)
            except AttributeError:
                raise ValueError("deprecation decorator must have \'func\' and \'name\' fields")
        else:
            raise ValueError("not a deprecation decorator")

    def check_error(self, current_version: VersionNumber) -> Optional[str]:
        """Return a user-facing error message if the deprecation is invalid.

        In order to be valid, a PythonDeprecation must have fields 'deprecated_in'
        and 'removed_in' both specified. Additionally, the current version of the software
        must be less than the expected removal version.

        Parameters
        ----------
        current_version: VersionNumber
            the current version of the software, against which to check the deprecation

        """
        if self.deprecated_in is None or self.removed_in is None:
            return "Both 'deprecated_in' and 'removed_in' must be specified"
        try:
            removed_version = VersionNumber(self.removed_in)
            if current_version >= removed_version:
                return "Current version, {}, exceeds expected removal version, {}" \
                    .format(current_version.version, removed_version.version)
        except ValueError as e:
            return f"Encountered an exception when parsing a version number: {e}"


class WrappedDeprecation:
    """A wrapper class that combines a deprecation and information about the node that contains it.

    This is useful for creating coherent error messages.

    Parameters
    ----------
    name: str
        the name of the method or class that has the deprecation decorator
    deprecation: PythonDeprecation
        a representation of the deprecation decorator
    """

    def __init__(self, name: str, deprecation: PythonDeprecation):
        self.name = name
        self.deprecation = deprecation

    def check_error(self, current_version: VersionNumber) -> Optional[str]:
        """Return an error message, if the deprecation is invalid for the current version.

        Parameters
        ----------
        current_version: VersionNumber
            the current version of the software, against which to check the deprecation

        Returns
        -------
        Optional[str]
            A human-readable error message, if the deprecation is invalid for this version

        """
        deprecation_error = self.deprecation.check_error(current_version)
        if deprecation_error is not None:
            return "{}: {}".format(self.name, deprecation_error)
