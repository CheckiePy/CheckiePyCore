import unittest

from unittest.mock import patch
from unittest.mock import mock_open

from acscore import metrics


class FileLengthTest(unittest.TestCase):
    def setUp(self):
        self.file_length = metrics.FileLength()
        self.data = {'5': 10, '35': 5, '100': 4, '105': 6}

    def test_count(self):
        with patch('acscore.metric.file_length.open', mock_open(read_data='hello\n\n\n\n\world\n')):
            result = self.file_length.count('')
        self.assertEqual({'5': 1}, result)

    def test_discretize(self):
        result = self.file_length.discretize(self.data)
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
        # Test with ok file
        discrete = self.file_length.discretize(self.data)
        result1 = self.file_length.inspect(discrete, {'10': 1})
        self.assertEqual({}, result1)

        # Test with too long file
        result2 = self.file_length.inspect(discrete, {'1000': 1})
        expected = {
            metrics.FileLength.TOO_MANY_LINES: {
                'message': metrics.FileLength.inspections[metrics.FileLength.TOO_MANY_LINES]
            }
        }
        self.assertEqual(expected, result2)
