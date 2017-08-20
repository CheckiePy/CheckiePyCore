import math


class FileLength:
    """ Number of lines in file. Verbose version doesn't require specific logic. """

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
        TOO_MANY_LINES: 'File too long. '
                        'According to the repo scan we recommend you to split this file into parts.'
    }

    def count(self, file, verbose=False):
        with open(file) as file:
            i = len(file.readlines())
        return {'{0}'.format(i): 1}

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0
        # Set initial values for each group to 0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0

        # Sum group values for each file
        for value, count in values.items():
            for group in self.discrete_groups:
                if group['from'] <= int(value) <= group['to']:
                    discrete_values[group['name']] += count
                    sum += count
                    continue

        # Normalize values
        for key, value in discrete_values.items():
            discrete_values[key] = value / sum

        return discrete_values

    def inspect(self, discrete, values):
        # Param values in this case should contain single value (for single file)
        value = list(values.keys())[0]

        # Find percent of files with length equal (or more) to length of value discrete group
        percent = 0.0
        for group in self.discrete_groups:
            if group['from'] <= int(value) <= group['to']:
                percent += discrete[group['name']]
            elif int(value) <= group['from']:
                # If file contains fewer lines it's ok
                percent += discrete[group['name']]
        inspections = {}

        # If less 1 % of files have approximately same length (or more) then generate message
        if percent < 0.01:
            inspections[self.TOO_MANY_LINES] = {'message': self.inspections[self.TOO_MANY_LINES]}

        return inspections
