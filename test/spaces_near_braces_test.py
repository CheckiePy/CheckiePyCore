import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics

from .table_test_case import TableTestCase


class SpacesNearBracesTest(unittest.TestCase):
    def setUp(self):
        self.data1 = {'spaces': 7, 'no_spaces': 33, 'new_lines': 0}
        self.data2 = {'spaces': 20, 'no_spaces': 80, 'new_lines': 0}
        self.data3 = {'spaces': 5, 'no_spaces': 5, 'new_lines': 0}
        self.spaces_near_braces = metrics.SpacesNearBraces()
        self.cases = [
            TableTestCase('a = { "a", "b", "c" }\n b = {"qwe": "asd", 1:2 } \n',
                          {'spaces': 3, 'no_spaces': 1, 'new_lines': 0}),
            TableTestCase('a = {\'5\', \'6\', "asd"}', {'spaces': 0, 'no_spaces': 2, 'new_lines': 0}),
            TableTestCase('while True\t{or not } :\n while True: pass', {'spaces': 1, 'no_spaces': 1, 'new_lines': 0}),
            TableTestCase('', {'spaces': 0, 'no_spaces': 0, 'new_lines': 0}),
            TableTestCase('a = "{some}"', {'spaces': 0, 'no_spaces': 0, 'new_lines': 0}),
            TableTestCase('a = {\n"hello": "world"\n}', {'spaces': 0, 'no_spaces': 0, 'new_lines': 1})
        ]

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.spaces_near_braces.open', mock_open(read_data=case.input)):
                result = self.spaces_near_braces.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}", but get "{2}"'.format(case.input, case.want, result))

    def test_discretize(self):
        result = self.spaces_near_braces.discretize(self.data1)
        self.assertEqual({'spaces': 0.175, 'no_spaces': 0.825, 'new_lines': 0.0}, result)

    def test_inspect(self):
            discrete = self.spaces_near_braces.discretize(self.data2)
            values = {
                'no_spaces': {
                    'count': 3,
                    'lines': [1, 2, 3],
                },
                'spaces': {
                    'count': 2,
                    'lines': [4, 5],
                },
                'new_lines': {
                    'count': 3,
                    'lines': [6, 7, 8],
                },
            }
            inspections = self.spaces_near_braces.inspect(discrete, values)
            expected = {
                metrics.SpacesNearBraces.NEED_NO_SPACES: {
                    'message': metrics.SpacesNearBraces.inspections[metrics.SpacesNearBraces.NEED_NO_SPACES],
                    'lines': [4, 5, 6, 7, 8],
                }
            }
            self.assertEqual(expected, inspections)