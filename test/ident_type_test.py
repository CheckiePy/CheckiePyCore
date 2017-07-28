import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class IndentTypeTest(unittest.TestCase):
    def setUp(self):
        self.indent_type = metrics.IndentType()
        self.files = [
            '    x = 1',
            '\ty = -3',
            'def f(): pass\n  x = 1\n\tclass C: pass\n',
        ]

    def test_count(self):
        with patch('acscore.metric.indent_type.open', mock_open(read_data=self.files[0])):
            result1 = self.indent_type.count('')
        self.assertEqual({'tabs': 0, 'spaces': 1}, result1)

        # with patch('acscore.metric.indent_type.open', mock_open(read_data=self.files[1])):
        #     result2 = self.indent_type.count('')
        # self.assertEqual({'tabs': 1, 'spaces': 0}, result2)

        # with patch('acscore.metric.indent_type.open', mock_open(read_data=self.files[2])):
        #     result3 = self.indent_type.count('')
        # self.assertEqual({'tabs': 0, 'spaces': 0}, result3)

    def test_discretize(self):
        pass

    def test_inspect(self):
        pass
