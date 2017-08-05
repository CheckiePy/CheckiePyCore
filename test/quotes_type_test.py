import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class QuotesTypeTest(unittest.TestCase):
    def setUp(self):
        self.data1 = {'single_quotes': 7, 'double_quotes': 3}
        self.data2 = {'single_quotes': 0, 'double_quotes': 0}
        self.data3 = {'single_quotes': 5, 'double_quotes': 5}
        self.quotes_type = metrics.QuotesType()
        self.files = [
            'a = ["a", "b", "c"]\n b = {"qwe": "asd", 1:2} \n',
            'a = [\'5\', \'6\', "asd"]',
            'a = "asdasd\'asdasd\'"',
            'while True:\n while True: pass',
            '',
        ]

    def test_count(self):
        with patch('acscore.metric.quotes_type.open', mock_open(read_data=self.files[0])):
            result1 = self.quotes_type.count('')
        self.assertEqual({'single_quotes': 0, 'double_quotes': 5}, result1)

        with patch('acscore.metric.quotes_type.open', mock_open(read_data=self.files[1])):
            result2 = self.quotes_type.count('')
        self.assertEqual({'single_quotes': 2, 'double_quotes': 1}, result2)

        with patch('acscore.metric.quotes_type.open', mock_open(read_data=self.files[2])):
            result3 = self.quotes_type.count('')
        self.assertEqual({'single_quotes': 0, 'double_quotes': 1}, result3)

        with patch('acscore.metric.quotes_type.open', mock_open(read_data=self.files[3])):
            result4 = self.quotes_type.count('')
        self.assertEqual({'single_quotes': 0, 'double_quotes': 0}, result4)

        with patch('acscore.metric.quotes_type.open', mock_open(read_data=self.files[4])):
            result4 = self.quotes_type.count('')
        self.assertEqual({'single_quotes': 0, 'double_quotes': 0}, result4)

    def test_discretize(self):
        result = self.quotes_type.discretize(self.data1)
        self.assertEqual({'single_quotes': 0.7, 'double_quotes': 0.3}, result)

    def test_inspect(self):
            discrete = self.quotes_type.discretize(self.data1)
            values = {
                'double_quotes': {
                    'count': 3,
                    'lines': [1, 2, 3],
                },
                'single_quotes': {
                    'count': 2,
                    'lines': [4, 5],
                },
            }
            inspections = self.quotes_type.inspect(discrete, values)
            expected = {
                metrics.QuotesType.NEED_TO_USE_SINGLE_QUOTES: {
                    'message': metrics.QuotesType.inspections[metrics.QuotesType.NEED_TO_USE_SINGLE_QUOTES],
                    'lines': [1, 2, 3],
                }
            }
            self.assertEqual(expected, inspections)