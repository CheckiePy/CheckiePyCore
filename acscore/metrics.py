from .metric.file_length import FileLength
from .metric.function_name_case import FunctionNameCase
from .metric.nesting_loops import NestingLoops
from .metric.class_name_case import ClassNameCase
from .metric.indent_type import IndentType


IMPLEMENTED_METRICS = [
    FileLength.__name__,
    FunctionNameCase.__name__,
    NestingLoops.__name__,
    ClassNameCase.__name__,
    IndentType.__name__,
]
