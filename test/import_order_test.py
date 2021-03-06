import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics

from .table_test_case import TableTestCase


class ImportOrderTest(unittest.TestCase):
    def setUp(self):
        self.import_order = metrics.ImportOrder()
        self.data = {'sorted': 14, 'not_sorted': 11, 'no_imports': 1}
        self.cases = [
            TableTestCase('import a\nimport c\nimport bb\nimport ba', {'not_sorted': 1}),
            TableTestCase('import A\nimport b\nimport c', {'sorted': 1}),
            TableTestCase('from a import b\nfrom c import g', {'sorted': 1}),
            TableTestCase('', {'sorted': 1}),
            TableTestCase('import b\na = "import a"', {'sorted': 1}),
            TableTestCase('c = 1\nb = 2', {'sorted': 1}),
            #TableTestCase('from a import z\nfrom c import g', {'not_sorted': 1}),
            #TableTestCase('from f import z\nfrom c import g', {'not_sorted': 1}),
        ]

    def test_count(self):
        for case in self.cases:
            with patch('acscore.metric.import_order.open', mock_open(read_data=case.input)):
                result = self.import_order.count('')
                self.assertEqual(case.want, result,
                                 'For input "{0}" want "{1}", but get "{2}"'.format(case.input, case.want, result))

    def test_discretize(self):
        result = self.import_order.discretize(self.data)
        expected = {
            'sorted': 14/26,
            'not_sorted': 11/26,
            'no_imports': 1/26,
        }
        self.assertEqual(expected, result)

    def test_inspect(self):

        discrete = self.import_order.discretize(self.data)
        result = self.import_order.inspect(discrete, {'not_sorted': 1})
        expected = {
            metrics.ImportOrder.NEED_SORTING: {
                'message': metrics.ImportOrder.inspections[metrics.ImportOrder.NEED_SORTING]
            }
        }
        self.assertEqual(expected, result)

