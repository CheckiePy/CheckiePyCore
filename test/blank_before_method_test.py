import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics

from .table_test_case import TableTestCase


class BlankBeforeMethodTest(unittest.TestCase):
    def setUp(self):
        self.blank_before_method = metrics.BlankBeforeMethod()
        self.data = {'0': 11, '1': 14, '2': 1}
        self.cases = [
            TableTestCase('class main:\n    def a(f,b):\n        pass\n\n    def b(f):\n        pass', {'1': 1}),
            TableTestCase('def main:\n    pass', {}),
            TableTestCase('class BlankBeforeMethodTest(unittest.TestCase):\n    def setUp(self):\n        pass\n'
                          '\n\n\n\n\n\n\n\n\n    def test_count(self):\n        pass\n\n    def new(self):\n       '
                          ' f.count = 0\n', {'3+' : 1, '1': 1}),
            TableTestCase('class main:\n    def a(f,b):\n        pass\n\n    def b(f):\n        pass', {'1': 1}),
            TableTestCase('def main:\n    pass', {}),
            TableTestCase('', {}),
            ]

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.blank_before_method.open', mock_open(read_data=case.input)):
                result = self.blank_before_method.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}", but get "{2}"'.format(case.input, case.want, result))

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.blank_before_method.open', mock_open(read_data=case.input)):
                result = self.blank_before_method.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}", but get "{2}"'.format(case.input, case.want, result))

    def test_discretize(self):
        result = self.blank_before_method.discretize(self.data)
        expected = {
            '0': 11/26,
            '1': 14/26,
            '2': 1/26,
            '3+': 0,
        }
        self.assertEqual(expected, result)

    def test_inspect(self):

        discrete = self.blank_before_method.discretize(self.data)
        result = self.blank_before_method.inspect(discrete, {'0': {
                                                                    'count': 1,
                                                                    'lines': [1]
                                                                    },
                                                             '3+': {
                                                                'count': 3,
                                                                'lines': [2, 3, 4]
                                                             }
                                                             })
        expected = {
            metrics.BlankBeforeMethod.TOO_MANY_LINES: {
                'message': metrics.BlankBeforeMethod.inspections[metrics.BlankBeforeMethod.TOO_MANY_LINES],
                'lines': [2, 3, 4],
            },
            metrics.BlankBeforeMethod.TOO_FEW_LINES: {
                'message': metrics.BlankBeforeMethod.inspections[metrics.BlankBeforeMethod.TOO_FEW_LINES],
                'lines': [1],
            }
        }
        self.assertEqual(expected, result)

