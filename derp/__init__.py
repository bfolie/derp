import ast
from derp.deprecation import PythonDeprecation

"""Tuple of ast node types that could contain deprecation warnings, either on themselves
or on a node some levels down. This (functions and classes) captures the typical cases.
I would not be surprised if there are situations in which a deprecation warning is missed
by this simplification, and this list is eventually expanded.
The safest thing to do would be to walk the entire ast tree. On the modestly-sized library
I tested derp on, walking the entire ast tree for every module took ~80 ms. Limiting the walker
to the relvant node types listed below caused it to take ~30 ms.
"""
RELEVANT_NODE_TYPES = (ast.Module, ast.ClassDef, ast.FunctionDef)

"""List of classes corresponding to ways a developer might mark a deprecation.
This currently only supports the @deprecated decorator from python's deprecation
library. For a discussion of how to add more possibilities, see discussion in deprecation.py
"""
DEPRECATION_TYPE_LIST = [PythonDeprecation]
