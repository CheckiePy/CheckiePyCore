import unittest
from acscore import metrics


class FunctionNameCaseTest(unittest.TestCase):
    def setUp(self):
        self.data = {'underscore': 100, 'camelcase': 10, 'other': 15}
        self.fnc = metrics.FunctionNameCase()

    def test_count(self):
        pass

    def test_count_verbose(self):
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
                'message': 'Underscore is used in 80.0% of code, but here camel case is used.', 'lines': [4, 5],
            },
            'no_style':
            {
                'message': 'Underscore and camel case mixed in same name.', 'lines': [6],
            }
        }
        self.assertEqual(expected, inspections)


class FileLengthTest(unittest.TestCase):
    def setUp(self):
        self.fl = metrics.FileLength()
        self.data = {5: 10, 35: 5, 100: 4, 105: 6}

    def test_count(self):
        pass

    def test_discretize(self):
        result = self.fl.discretize(self.data)
        expected = {
            'From0To40': 0.6,
            'From41To200': 0.4,
            'From201To600': 0.0,
            'From601To1500': 0.0,
            'From1501To5000': 0.0,
            'From5000ToInf': 0.0,
        }
        self.assertEqual(expected, result)

    def test_inspect(self):
        discrete = self.fl.discretize(self.data)
        result1 = self.fl.inspect(discrete, {10: 1})
        self.assertEqual({}, result1)
        result2 = self.fl.inspect(discrete, {1000: 1})
        expected = {
            'too_many_lines':
            {
                'message': 'Less than 5% of files have approximately same size.'
                           ' Maybe you need to split this file in parts.'
            }
        }
        self.assertEqual(expected, result2)

if __name__ == '__main__':
    unittest.main()
