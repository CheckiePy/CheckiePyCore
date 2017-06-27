import unittest
from acscore import metrics
from acscore import analyzer


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
        self.data = {'5': 10, '35': 5, '100': 4, '105': 6}

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
        result1 = self.fl.inspect(discrete, {'10': 1})
        self.assertEqual({}, result1)
        result2 = self.fl.inspect(discrete, {'1000': 1})
        expected = {
            'too_many_lines':
                {
                    'message': 'Less than 5% of files have approximately same size.'
                               ' Maybe you need to split this file in parts.'
                }
        }
        self.assertEqual(expected, result2)


class NestingLoopsTest(unittest.TestCase):
    def setUp(self):
        self.nl = metrics.NestingLoops()
        self.data1 = {'0': 7, '2': 2, '5': 1}
        self.data2 = {'0': 15, '4': 5, '7': 3, '15': 2}

    def test_count(self):
        pass

    def test_discretize(self):
        result1 = self.nl.discretize(self.data1)
        expected1 = {
            'From0To2': 0.9,
            'From3To5': 0.1,
            'From6To10': 0.0,
            'From11ToInf': 0.0,
        }
        self.assertEqual(expected1, result1)
        result2 = self.nl.discretize(self.data2)
        expected2 = {
            'From0To2': 0.6,
            'From3To5': 0.2,
            'From6To10': 0.12,
            'From11ToInf': 0.08,
        }
        self.assertEqual(expected2, result2)

    def test_inspect(self):
        discrete = self.nl.discretize(self.data1)
        result1 = self.nl.inspect(discrete, {'0': 1})
        self.assertEqual({}, result1)
        result2 = self.nl.inspect(discrete, {'1000': 1})
        expected = {
            'too_many_loops':
                {
                    'message': 'Less than 5% of files have approximately same depth of loops.'
                               ' Maybe you need to make less loops.'
                }
        }
        self.assertEqual(expected, result2)


class AnalyzerTest(unittest.TestCase):
    def test_inspect(self):
        initial_metrics = {
            'FunctionNameCase': {'underscore': 100, 'camelcase': 10, 'other': 15},
            'FileLength': {'5': 10, '35': 5, '100': 4, '105': 6},
        }
        a = analyzer.Analyzer(initial_metrics)
        file_metrics = {
            'FunctionNameCase':
                {
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
                },
            'FileLength': {'1000': 1},
        }
        inspections = a.inspect(file_metrics)
        expected = {
            'FunctionNameCase':
                {
                    'no_style':
                        {
                            'message': 'Underscore and camel case mixed in same name.', 'lines': [6],
                        },
                    'need_to_use_underscore':
                        {
                            'message': 'Underscore is used in 80.0% of code, but here camel case is used.',
                            'lines': [4, 5],
                        },
                },
            'FileLength':
                {
                    'too_many_lines':
                        {
                            'message': 'Less than 5% of files have approximately same size. '
                                       'Maybe you need to split this file in parts.',
                        },
                },
        }
        self.assertEqual(expected, inspections)


if __name__ == '__main__':
    unittest.main()
