from acscore.metric.file_length import FileLength
from acscore.metric.function_name_case import FunctionNameCase
from acscore.metric.nesting_loops import NestingLoops
from acscore.metric.function_length import FunctionLength
from acscore.metric.class_name_case import ClassNameCase
from acscore.metric.max_function_length import MaxFunctionLength
from acscore.metric.ident_type import IndentType


IMPLEMENTED_METRICS = [
    FileLength.__name__,
    FunctionNameCase.__name__,
    NestingLoops.__name__,
    FunctionLength.__name__,
    ClassNameCase.__name__,
    MaxFunctionLength.__name__,
    IndentType.__name__,
]
