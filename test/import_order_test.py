import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class ImportOrderTest(unittest.TestCase):
    def setUp(self):
        self.import_order = metrics.ImportOrder()
        self.data = {'sorted': 14, 'not_sorted': 11, 'no_imports': 1}

    def test_count(self):
        with patch('acscore.metric.import_order.open', mock_open(read_data='import a\nimport c\nimport bb\nimport ba')):
            result = self.import_order.count('')
        self.assertEqual({'not_sorted': 1}, result)

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

