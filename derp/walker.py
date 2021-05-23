import ast
from typing import Optional, Iterator, Any, Callable, List

from derp import RELEVANT_NODE_TYPES, DEPRECATION_TYPE_LIST
from derp.deprecation import PythonDeprecation, WrappedDeprecation
from derp.version_number import VersionNumber


def _parse_deprecation(decorator: ast.AST) -> Optional[PythonDeprecation]:
    """Parse a decorator node to see if it represents a deprecation of some sort.

    If the decorator can be parsed to multiple types of deprecations, only the first one
    will be returned.

    Parameters
    ----------
    decorator: ast.AST
        A node of a syntax tree that is *expected* to be a decorator of type ast.Call

    Returns
    -------
    Optional[Deprecation]
        A deprecation representation of the decorator, if applicable

    """
    deprecation = None
    for deprecation_type in DEPRECATION_TYPE_LIST:
        try:
            deprecation = deprecation_type(decorator)
        except ValueError:
            pass
        if deprecation is not None:
            break
    return deprecation


def _get_deprecation(node: ast.AST) -> Optional[WrappedDeprecation]:
    """Get a deprecation decorator child of a given node, if one exists.

    If there are multiple deprecation decorators attached to the node, only the first one
    will be returned.

    Parameters
    ----------
    node: ast.AST
        A node of a syntax tree

    Returns
    -------
    Optional[WrappedDeprecation]
        The deprecation, if it exists, wrapped with metadata

    """
    try:
        decorators = node.decorator_list
        this_name = node.name
        if isinstance(decorators, list):
            for decorator in decorators:
                deprecation = _parse_deprecation(decorator)
                if deprecation is not None:
                    return WrappedDeprecation(this_name, deprecation)
    except AttributeError:
        pass


def _iter_relevant_children(node: ast.AST):
    """Yield all relevant direct child nodes of *node*.

    "Relevant" children are those that may contain deprecations.

    Parameters
    ----------
    node: ast.AST
        A node of a syntax tree

    """
    for name, field in ast.iter_fields(node):
        if isinstance(field, RELEVANT_NODE_TYPES):
            yield field
        elif isinstance(field, list):
            for item in field:
                if isinstance(item, RELEVANT_NODE_TYPES):
                    yield item


def _yield_deprecation_message(node: ast.AST, current_version: VersionNumber) -> Optional[str]:
    """Filter nodes that correspond to an invalid deprecation, and return an error message.

    Parameters
    ----------
    node: ast.AST
        A node of a syntax tree
    current_version: VersionNumber
        Current version of the software, to compare the deprecation against

    Returns
    -------
    str
        An error message if the node corresponds to an invalid deprecation

    """
    maybe_deprecation = _get_deprecation(node)
    if maybe_deprecation is not None:
        return maybe_deprecation.check_error(current_version)
    else:
        return None


def _walk_nodes_filter_transform(
        node: ast.AST,
        filter_transform: Callable[[ast.AST], Optional[Any]] = lambda node: node
) -> Iterator[Any]:
    """Walk all nodes of a syntax tree, applying an optional filter and transformation.

    Parameters
    ----------
    node: ast.AST
        The root of the tree
    filter_transform: Callable[[ast.AST], Optional[Any]]
        A method that accepts an ast node and returns either a function of that node or None

    Returns
    -------
    Iterator[Any]
        An iterator over the transformed version of the nodes that pass the filter

    """
    from collections import deque
    todo = deque([node])
    while todo:
        node = todo.popleft()
        todo.extend(_iter_relevant_children(node))
        maybe_result = filter_transform(node)
        if maybe_result is not None:
            yield maybe_result


def collect_deprecation_errors(
        filepath: str,
        current_version: VersionNumber
) -> Optional[List[str]]:
    """Collect all deprecation errors in a given module.

    Parameters
    ----------
    filepath: str
        path to a python module
    current_version: VersionNumber
        current version of the software against which to check deprecation removal
    """
    with open(filepath) as source:
        tree = ast.parse(source.read())
        deprecation_generator = _walk_nodes_filter_transform(
            tree,
            lambda node: _yield_deprecation_message(node, current_version)
        )
        return list(deprecation_generator)
