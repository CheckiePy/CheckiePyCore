import math


class FileLength:
    TOO_MANY_LINES = 'too_many_lines'
    discrete_groups = [
        {
            'name': 'From0To40',
            'from': 0,
            'to': 40,
        },
        {
            'name': 'From41To200',
            'from': 41,
            'to': 200,
        },
        {
            'name': 'From201To600',
            'from': 201,
            'to': 600,
        },
        {
            'name': 'From601To1500',
            'from': 601,
            'to': 1500,
        },
        {
            'name': 'From1501To5000',
            'from': 1501,
            'to': 5000,
        },
        {
            'name': 'From5000ToInf',
            'from': 5000,
            'to': math.inf,
        },
    ]
    inspections = {
        TOO_MANY_LINES: ' File too long '
                        ' According to the repo scan we recommend you to split this file into parts. '
    }

    """ Number of lines in file. Verbose version doesn't require specific logic. """

    def count(self, file, verbose=False):
        i = 0
        with open(file) as f:
            for i, _ in enumerate(f, 1):
                pass
        return {'{0}'.format(i): 1}

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0
        for value, count in values.items():
            for group in self.discrete_groups:
                if group['from'] <= int(value) <= group['to']:
                    discrete_values[group['name']] += count
                    sum += count
                    continue
        for key, value in discrete_values.items():
            discrete_values[key] = value / sum
        return discrete_values

    def inspect(self, discrete, values):
        value = list(values.keys())[0]
        percent = 0.0
        for group in self.discrete_groups:
            if group['from'] <= int(value) <= group['to']:
                value_group = group
                percent += discrete[group['name']]
            elif int(value) <= group['from']:
                # If file contains fewer lines it's ok
                percent += discrete[group['name']]
        inspections = {}
        too_many_lines = 'too_many_lines'
        if percent < 0.05:
            inspections[too_many_lines] = {'message': self.inspections[too_many_lines].format(5)}
        elif percent < 0.1:
            inspections[too_many_lines] = {'message': self.inspections[too_many_lines].format(10)}
        elif percent < 0.2:
            inspections[too_many_lines] = {'message': self.inspections[too_many_lines].format(20)}
        return inspections
