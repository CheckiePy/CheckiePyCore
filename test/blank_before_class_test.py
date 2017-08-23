import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics

from .table_test_case import TableTestCase


class BlankBeforeClassTest(unittest.TestCase):
    def setUp(self):
        self.blank_before_class = metrics.BlankBeforeClass()
        self.data = {'0': 14, '1': 11, '3+': 1}
        self.cases = [
            TableTestCase('class c1:\n\n\nclass a(f,b):\n    a = 0\ndef asd:\n    pass\n\n\nclass b:', {'2': 2}),
            TableTestCase('class a(unittest.TestCase):\n    def setUp(self):\n    newclassdefinition = 1\n\nclass b(asd):\n\nclass_count=1\n    pass\n\n', {'1': 1}),
            TableTestCase('from a import b\nfrom c import g\ndef f:\n    pass\ndef f1:\n    '
                          'def f2:\n         pass\n    \n\n', {}),
            TableTestCase('', {}),
            TableTestCase('class a:\n    def a:\n        a = 0\n\n\n\n\n\ndef basd(da):\n    as = 0\n\nclass fsdf:\n    '
                          'bbb=0\n    pass\n\n\n\n\n\n\ndef f:\n    pass', {'1': 1})
            ]

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.blank_before_class.open', mock_open(read_data=case.input)):
                result = self.blank_before_class.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}", but get "{2}"'.format(case.input, case.want, result))

    def test_discretize(self):
        result = self.blank_before_class.discretize(self.data)
        expected = {
            '0': 14/26,
            '1': 11/26,
            '2': 0,
            '3+': 1/26,
        }
        self.assertEqual(expected, result)

    def test_inspect(self):

        discrete = self.blank_before_class.discretize(self.data)
        result = self.blank_before_class.inspect(discrete, {'2': {
                                                                    'count': 2,
                                                                    'lines': [1, 3]
                                                                    }
                                                             })
        expected = {
            metrics.BlankBeforeClass.TOO_MANY_LINES: {
                'message': metrics.BlankBeforeClass.inspections[metrics.BlankBeforeClass.TOO_MANY_LINES],
                'lines': [1, 3],
            }
        }
        self.assertEqual(expected, result)

