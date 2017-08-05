import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class SpacesNearSquareBracketsTest(unittest.TestCase):
    def setUp(self):
        self.data1 = {'spaces': 7, 'no_spaces': 33}
        self.data2 = {'spaces': 20, 'no_spaces': 80}
        self.data3 = {'spaces': 5, 'no_spaces': 5}
        self.spaces_near_square_brackets = metrics.SpacesNearSquareBrackets()
        self.files = [
            'a = [ "a", "b", ["c"] ]\n b = ["qwe": "asd", 1:2] \n',
            'a = [\'5\', \'6\', "asd"]',
            'while True(or not):\n while True: pass',
            '',
        ]

    def test_count(self):
        with patch('acscore.metric.spaces_near_square_brackets.open', mock_open(read_data=self.files[0])):
            result1 = self.spaces_near_square_brackets.count('')
        self.assertEqual({'spaces': 2, 'no_spaces': 4}, result1)

        with patch('acscore.metric.spaces_near_square_brackets.open', mock_open(read_data=self.files[1])):
            result2 = self.spaces_near_square_brackets.count('')
        self.assertEqual({'spaces': 0, 'no_spaces': 2}, result2)

        with patch('acscore.metric.spaces_near_square_brackets.open', mock_open(read_data=self.files[2])):
            result3 = self.spaces_near_square_brackets.count('')
        self.assertEqual({'spaces': 0, 'no_spaces': 0}, result3)

        with patch('acscore.metric.spaces_near_square_brackets.open', mock_open(read_data=self.files[3])):
            result4 = self.spaces_near_square_brackets.count('')
        self.assertEqual({'spaces': 0, 'no_spaces': 0}, result4)

    def test_discretize(self):
        result = self.spaces_near_square_brackets.discretize(self.data1)
        self.assertEqual({'spaces': 0.175, 'no_spaces': 0.825}, result)

    def test_inspect(self):
            discrete = self.spaces_near_square_brackets.discretize(self.data2)
            values = {
                'no_spaces': {
                    'count': 3,
                    'lines': [1, 2, 3],
                },
                'spaces': {
                    'count': 2,
                    'lines': [4, 5],
                },
            }
            inspections = self.spaces_near_square_brackets.inspect(discrete, values)
            expected = {
                metrics.SpacesNearSquareBrackets.NEED_NO_SPACES: {
                    'message': metrics.SpacesNearSquareBrackets.inspections[metrics.SpacesNearSquareBrackets.NEED_NO_SPACES],
                    'lines': [4, 5],
                }
            }
            self.assertEqual(expected, inspections)