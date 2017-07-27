import unittest

from acscore import metrics
from acscore import analyzer


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
                            'message': metrics.FunctionNameCase.inspections[metrics.FunctionNameCase.NO_STYLE], 'lines': [6],
                        },
                    'need_to_use_underscore':
                        {
                            'message': metrics.FunctionNameCase.inspections[metrics.FunctionNameCase.NEED_TO_USE_UNDERSCORE],
                            'lines': [4, 5],
                        },
                },
            'FileLength':
                {
                    'too_many_lines':
                        {
                            'message': metrics.FileLength.inspections[metrics.FileLength.TOO_MANY_LINES],
                        },
                },
        }
        self.assertEqual(expected, inspections)
