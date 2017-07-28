from .metric.file_length import FileLength
from .metric.function_name_case import FunctionNameCase
from .metric.nesting_loops import NestingLoops
from .metric.function_length import FunctionLength
from .metric.class_name_case import ClassNameCase
from .metric.max_function_length import MaxFunctionLength
from .metric.ident_type import IndentType


IMPLEMENTED_METRICS = [
    FileLength.__name__,
    FunctionNameCase.__name__,
    NestingLoops.__name__,
    FunctionLength.__name__,
    ClassNameCase.__name__,
    MaxFunctionLength.__name__,
    IndentType.__name__,
]
