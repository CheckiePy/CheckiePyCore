import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class IndentTypeTest(unittest.TestCase):
    def setUp(self):
        self.data = {'tabs': 8, 'spaces': 2}
        self.indent_type = metrics.IndentType()
        self.files = [
            '    x = 1\n',
            '\ty = -3\n',
            'def f(): pass\n  x = 1\n\tclass C: pass\n',
        ]

    def test_count(self):
        with patch('acscore.metric.indent_type.open', mock_open(read_data=self.files[0])):
            result1 = self.indent_type.count('')
        self.assertEqual({'tabs': 0, 'spaces': 1}, result1)

        with patch('acscore.metric.indent_type.open', mock_open(read_data=self.files[1])):
            result2 = self.indent_type.count('')
        self.assertEqual({'tabs': 1, 'spaces': 0}, result2)

        with patch('acscore.metric.indent_type.open', mock_open(read_data=self.files[2])):
            result3 = self.indent_type.count('')
        self.assertEqual({'tabs': 0, 'spaces': 0}, result3)

    def test_discretize(self):
        result = self.indent_type.discretize(self.data)
        self.assertEqual({'tabs': 0.8, 'spaces': 0.2}, result)

    def test_inspect(self):
        discrete = self.indent_type.discretize(self.data)
        values = {'tabs': 0, 'spaces': 1}
        inspections = self.indent_type.inspect(discrete, values)
        expected = {
            metrics.IndentType.NEED_TO_USE_TABS: {
                'message': metrics.IndentType.inspections[metrics.IndentType.NEED_TO_USE_TABS]
            }
        }
        self.assertEqual(expected, inspections)
