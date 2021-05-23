import ast
from .deprecation import PythonDeprecation

RELEVANT_NODE_TYPES = (ast.Module, ast.ClassDef, ast.FunctionDef)
DEPRECATION_TYPE_LIST = [PythonDeprecation]
