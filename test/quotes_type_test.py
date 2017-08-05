import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics

from .table_test_case import TableTestCase


class QuotesTypeTest(unittest.TestCase):
    def setUp(self):
        self.data1 = {'single_quotes': 7, 'double_quotes': 3}
        self.data2 = {'single_quotes': 0, 'double_quotes': 0}
        self.data3 = {'single_quotes': 5, 'double_quotes': 5}
        self.quotes_type = metrics.QuotesType()
        self.cases = [
            TableTestCase('a = ["a", "b", "c"]\n b = {"qwe": "asd", 1:2} \n', {'single_quotes': 0, 'double_quotes': 5}),
            TableTestCase('a = [\'5\', \'6\', "asd"]', {'single_quotes': 2, 'double_quotes': 1}),
            TableTestCase('a = "asdasd\'asdasd\'"', {'single_quotes': 0, 'double_quotes': 1}),
            TableTestCase('while True:\n while True: pass', {'single_quotes': 0, 'double_quotes': 0}),
            TableTestCase('', {'single_quotes': 0, 'double_quotes': 0}),
            TableTestCase('s = \'What is "Pineapple"?\'', {'single_quotes': 1, 'double_quotes': 0}),
            TableTestCase('s = "Let\'s go"', {'single_quotes': 0, 'double_quotes': 1}),
            # TODO
            #TableTestCase('s = "Hello, \"foo \'bar\'\"', {'single_quotes': 0, 'double_quotes': 1}),
            #TableTestCase('s = \'hello ,\'foo "bar"\'', {'single_quotes': 1, 'double_quotes': 0}),
        ]

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.quotes_type.open', mock_open(read_data=case.input)):
                result = self.quotes_type.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}, but get "{2}"'.format(case.input, case.want, result))

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