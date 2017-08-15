import unittest

# Imports are implicitly used by unittest package
from test.file_length_test import FileLengthTest
from test.function_name_case_test import FunctionNameCaseTest
from test.class_name_case_test import ClassNameCaseTest
from test.indent_type_test import IndentTypeTest
from test.nesting_loops_test import NestingLoopsTest
from test.analyzer_test import AnalyzerTest
from test.quotes_type_test import QuotesTypeTest
from test.spaces_near_round_brackets_test import SpacesNearRoundBracketsTest
from test.spaces_near_braces_test import SpacesNearBracesTest
from test.spaces_near_square_brackets_test import SpacesNearSquareBracketsTest
from test.import_order_test import ImportOrderTest

if __name__ == '__main__':
    unittest.main()
