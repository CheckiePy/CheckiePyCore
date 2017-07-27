import unittest

from acscore import metrics


class FunctionNameCaseTest(unittest.TestCase):
    def setUp(self):
        self.data = {'underscore': 100, 'camelcase': 10, 'other': 15}
        self.fnc = metrics.FunctionNameCase()

    def test_count(self):
        # TODO
        pass

    def test_count_verbose(self):
        # TODO
        pass

    def test_discretize(self):
        result = self.fnc.discretize(self.data)
        self.assertEqual({'other': 0.12, 'underscore': 0.8, 'camelcase': 0.08}, result)

    def test_inspect(self):
        discrete = self.fnc.discretize(self.data)
        values = {
            'underscore':
                {
                    'count': 3,
                    'lines': [1, 2, 3],
                },
            'camelcase':
                {
                    'count': 2,
                    'lines': [4, 5],
                },
            'other':
                {
                    'count': 1,
                    'lines': [6],
                },
        }
        inspections = self.fnc.inspect(discrete, values)
        expected = {
            'need_to_use_underscore':
                {
                    'message': metrics.FunctionNameCase.inspections[metrics.FunctionNameCase.NEED_TO_USE_UNDERSCORE], 'lines': [4, 5],
                },
            'no_style':
                {
                    'message': metrics.FunctionNameCase.inspections[metrics.FunctionNameCase.NO_STYLE], 'lines': [6],
                }
        }
        self.assertEqual(expected, inspections)
