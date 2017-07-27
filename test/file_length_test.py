import unittest

from acscore import metrics


class FileLengthTest(unittest.TestCase):
    def setUp(self):
        self.fl = metrics.FileLength()
        self.data = {'5': 10, '35': 5, '100': 4, '105': 6}

    def test_count(self):
        # TODO
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
                    'message': metrics.FileLength.inspections[metrics.FileLength.TOO_MANY_LINES]
                }
        }
        self.assertEqual(expected, result2)
