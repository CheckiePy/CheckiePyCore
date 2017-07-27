import unittest

from acscore import metrics


class NestingLoopsTest(unittest.TestCase):
    def setUp(self):
        self.nl = metrics.NestingLoops()
        self.data1 = {'0': 7, '2': 2, '5': 1}
        self.data2 = {'0': 15, '4': 5, '7': 3, '15': 2}

    def test_count(self):
        # TODO
        pass

    def test_discretize(self):
        result1 = self.nl.discretize(self.data1)
        expected1 = {
            'From0To2': 0.9,
            'From3To4': 0.0,
            'From5ToInf': 0.1,
        }
        self.assertEqual(expected1, result1)
        result2 = self.nl.discretize(self.data2)
        expected2 = {
            'From0To2': 0.6,
            'From3To4': 0.2,
            'From5ToInf': 0.2,
        }
        self.assertEqual(expected2, result2)

    # TODO: uncomment and fix bug
    # def test_inspect(self):
    #     discrete = self.nl.discretize(self.data1)
    #     result1 = self.nl.inspect(discrete, {'0': 1})
    #     self.assertEqual({}, result1)
    #     result2 = self.nl.inspect(discrete, {'1000': 1})
    #     expected = {
    #         'too_many_loops':
    #             {
    #                 'message': 'Less than 5% of files have approximately same depth of loops.'
    #                            ' Maybe you need to make less loops.'
    #             }
    #     }
    #     self.assertEqual(expected, result2)
