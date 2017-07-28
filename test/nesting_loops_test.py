import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class NestingLoopsTest(unittest.TestCase):
    def setUp(self):
        self.data1 = {'0': 7, '2': 2, '5': 1}
        self.data2 = {'0': 15, '4': 5, '7': 3, '15': 2}
        self.nesting_loops = metrics.NestingLoops()
        self.files = [
            'for x in range(10):\n for y in range(20): pass\n\nfor x in range(1):\n for y in range(2):\n  for z in range(3): pass\n',
            'for x in range(10):\n for y in range(20): pass\nfor x in range(1):\n for y in range(2):\n  for z in range(3): pass',
            'while True:\n while True: pass',
            'for x in range(1): pass\nwhile True: pass\nfor y in range(3): pass\n',
            '',
        ]

    def test_count(self):
        with patch('acscore.metric.nesting_loops.open', mock_open(read_data=self.files[0])):
            result1 = self.nesting_loops.count('')
        self.assertEqual({'2': 1, '3': 1}, result1)

        with patch('acscore.metric.nesting_loops.open', mock_open(read_data=self.files[1])):
            result2 = self.nesting_loops.count('')
        self.assertEqual({'2': 1, '3': 1}, result2)

        with patch('acscore.metric.nesting_loops.open', mock_open(read_data=self.files[2])):
            result3 = self.nesting_loops.count('')
        self.assertEqual({'2': 1}, result3)

        with patch('acscore.metric.nesting_loops.open', mock_open(read_data=self.files[3])):
            result4 = self.nesting_loops.count('')
        self.assertEqual({'1': 3}, result4)

        with patch('acscore.metric.nesting_loops.open', mock_open(read_data=self.files[4])):
            result5 = self.nesting_loops.count('')
        self.assertEqual({}, result5)

    def test_discretize(self):
        result1 = self.nesting_loops.discretize(self.data1)
        expected1 = {
            'From0To2': 0.9,
            'From3To4': 0.0,
            'From5ToInf': 0.1,
        }
        self.assertEqual(expected1, result1)
        result2 = self.nesting_loops.discretize(self.data2)
        expected2 = {
            'From0To2': 0.6,
            'From3To4': 0.2,
            'From5ToInf': 0.2,
        }
        self.assertEqual(expected2, result2)

    # TODO: uncomment and fix bug
    # def test_inspect(self):
    #     discrete = self.nl.discretize(self.data1)
    #     result1 = self.nl.inspect(discrete, {'0': 1})
    #     self.assertEqual({}, result1)
    #     result2 = self.nl.inspect(discrete, {'1000': 1})
    #     expected = {
    #         'too_many_loops':
    #             {
    #                 'message': 'Less than 5% of files have approximately same depth of loops.'
    #                            ' Maybe you need to make less loops.'
    #             }
    #     }
    #     self.assertEqual(expected, result2)
