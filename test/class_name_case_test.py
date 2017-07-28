import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class ClassNameCaseTest(unittest.TestCase):
    def setUp(self):
        self.data = {'underscore': 100, 'camelcase': 10, 'other': 15}
        self.class_name_case = metrics.ClassNameCase()
        self.files = [
            'class helloName: pass\n\nclass Kek: pass\n\n\nclass _hidden: pass\n',
            'class OkName: pass\nclass Very_Strange: pass\nclass looks__like: pass\n',
            'class yet_another_class_name: pass\n\nclass yet: pass\nclass TesT: pass\n',
        ]

    def test_count(self):
        with patch('acscore.metric.class_name_case.open', mock_open(read_data=self.files[0])):
            result1 = self.class_name_case.count('')
        expected1 = {
            'other': 1,
            'camelcase': 2,
            'underscore': 0,
        }
        self.assertEqual(expected1, result1)

        with patch('acscore.metric.class_name_case.open', mock_open(read_data=self.files[1])):
            result2 = self.class_name_case.count('')
        expected2 = {
            'other': 2,
            'camelcase': 1,
            'underscore': 0,
        }
        self.assertEqual(expected2, result2)

        with patch('acscore.metric.class_name_case.open', mock_open(read_data=self.files[2])):
            result3 = self.class_name_case.count('')
        expected3 = {
            'other': 0,
            'camelcase': 1,
            'underscore': 1,
        }
        self.assertEqual(expected3, result3)

    def test_count_verbose(self):
        with patch('acscore.metric.class_name_case.open', mock_open(read_data=self.files[0])):
            result1 = self.class_name_case.count('', True)
        expected1 = {
            'other': {
                'count': 1,
                'lines': [6],
            },
            'camelcase': {
                'count': 2,
                'lines': [1, 3],
            },
            'underscore': {
                'count': 0,
                'lines': [],
            },
        }
        self.assertEqual(expected1, result1)

        with patch('acscore.metric.class_name_case.open', mock_open(read_data=self.files[1])):
            result2 = self.class_name_case.count('', True)
        expected2 = {
            'other': {
                'count': 2,
                'lines': [2, 3],
            },
            'camelcase': {
                'count': 1,
                'lines': [1],
            },
            'underscore': {
                'count': 0,
                'lines': [],
            },
        }
        self.assertEqual(expected2, result2)

        with patch('acscore.metric.class_name_case.open', mock_open(read_data=self.files[2])):
            result3 = self.class_name_case.count('', True)
        expected3 = {
            'other': {
                'count': 0,
                'lines': [],
            },
            'camelcase': {
                'count': 1,
                'lines': [4],
            },
            'underscore': {
                'count': 1,
                'lines': [1],
            },
        }
        self.assertEqual(expected3, result3)

    def test_discretize(self):
        result = self.class_name_case.discretize(self.data)
        self.assertEqual({'other': 0.12, 'underscore': 0.8, 'camelcase': 0.08}, result)

    def test_inspect(self):
        discrete = self.class_name_case.discretize(self.data)
        values = {
            'underscore': {
                'count': 3,
                'lines': [1, 2, 3],
            },
            'camelcase': {
                'count': 2,
                'lines': [4, 5],
            },
            'other': {
                'count': 1,
                'lines': [6],
            },
        }
        inspections = self.class_name_case.inspect(discrete, values)
        expected = {
            metrics.ClassNameCase.NEED_TO_USE_UNDERSCORE: {
                'message': metrics.ClassNameCase.inspections[metrics.ClassNameCase.NEED_TO_USE_UNDERSCORE],
                'lines': [4, 5],
            },
            metrics.ClassNameCase.NO_STYLE: {
                'message': metrics.ClassNameCase.inspections[metrics.ClassNameCase.NO_STYLE],
                'lines': [6],
            }
        }
        self.assertEqual(expected, inspections)
