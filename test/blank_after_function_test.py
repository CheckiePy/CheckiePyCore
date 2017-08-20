import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics

from .table_test_case import TableTestCase


class BlankAfterFunctionTest(unittest.TestCase):
    def setUp(self):
        self.blank_after_function = metrics.BlankAfterFunction()
        self.data = {'0': 14, '1': 11, '3+': 1}
        self.cases = [
            TableTestCase('def main:\n    pass\n\ndef a(f,b):\n    pass', {'1': 1}),
            TableTestCase('def main:\n    pass', {}),
            TableTestCase('from a import b\nfrom c import g\ndef f:\n    pass\ndef f1:\n    '
                          'def f2:\n         pass\n    \n\n', {'0': 2}),
            TableTestCase('', {}),
            TableTestCase('def main\n\n    pass\n\n\n\n\n\n\ndef f:\n    pass', {'3+': 1})
            ]

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.blank_after_function.open', mock_open(read_data=case.input)):
                result = self.blank_after_function.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}", but get "{2}"'.format(case.input, case.want, result))

    def test_discretize(self):
        result = self.blank_after_function.discretize(self.data)
        expected = {
            '0': 14/26,
            '1': 11/26,
            '2': 0,
            '3+': 1/26,
        }
        self.assertEqual(expected, result)

    def test_inspect(self):

        discrete = self.blank_after_function.discretize(self.data)
        result = self.blank_after_function.inspect(discrete, {'2': {
                                                                    'count': 1,
                                                                    'lines': [1]
                                                                    }
                                                             })
        expected = {
            metrics.BlankAfterFunction.TOO_MANY_LINES: {
                'message': metrics.BlankAfterFunction.inspections[metrics.BlankAfterFunction.TOO_MANY_LINES],
                'lines': [1],
            }
        }
        self.assertEqual(expected, result)

