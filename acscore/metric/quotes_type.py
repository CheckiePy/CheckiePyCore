class QuotesType:
    """ Checks whether quotation marks are double or single in source file. """

    NEED_TO_USE_SINGLE_QUOTES = 'need_to_use_single_quotes'
    NEED_TO_USE_DOUBLE_QUOTES = 'need_to_use_double_quotes'

    discrete_groups = [
        { 'name': 'single_quotes' },
        { 'name': 'double_quotes' },
    ]

    inspections = {
        NEED_TO_USE_SINGLE_QUOTES: 'Mostly single quotes are used in the source code, '
                                   'maybe you need to change double quotes here.',
        NEED_TO_USE_DOUBLE_QUOTES: 'Mostly double quotes are used in the source code, '
                                   'maybe you need to change single quotes here.',
    }

    def count(self, file, verbose=False):
        # Count all quotes that are single or double
        with open(file) as f:
            single_quotes_count = 0
            double_quotes_count = 0
            single_quotes_lines = []
            double_quotes_lines = []
            line_number = 0
            for line in f.readlines():
                line_number += 1
                for i in line:
                    if i == '\'':
                        single_quotes_count += 1
                        single_quotes_lines.append(line_number)
                    if i == '\"':
                        double_quotes_count += 1
                        double_quotes_lines.append(line_number)

        single_quotes_lines.sort()
        unique_single_quotes_lines = []
        for i in range(len(single_quotes_lines) - 1):
            if i == 0 or single_quotes_lines[i] != single_quotes_lines[i-1]:
                unique_single_quotes_lines.append(single_quotes_lines[i])

        # Getting unique values for lines
        double_quotes_lines.sort()
        unique_double_quotes_lines = []
        for i in range(len(double_quotes_lines) - 1):
            if i == 0 or double_quotes_lines[i] != double_quotes_lines[i - 1]:
                unique_double_quotes_lines.append(double_quotes_lines[i])

        # Form result
        result = {
            'single_quotes': single_quotes_count,
            'double_quotes': double_quotes_count,
        }

        if verbose:
            result['single_quotes'] = {
                'count': single_quotes_count,
                'lines': unique_single_quotes_lines,
            }
            result['double_quotes'] = {
                'count': double_quotes_count,
                'lines': unique_double_quotes_lines,
            }
        return result

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0

        # Set initial values for groups to 0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0

        # Sum values for each group
        for group, count in values.items():
            discrete_values[group] = count
            sum += count

        # Normalize
        for group, count in discrete_values.items():
            if sum != 0:
                discrete_values[group] = count / sum

        return discrete_values

    def inspect(self, discrete, values):
        for_discretization = {}

        for key, value in values.items():
            for_discretization[key] = value['count']

        file_discrete = self.discretize(for_discretization)

        # Check if single or double quotes are prevailing
        is_single_quote = False
        if discrete['single_quotes'] > discrete['double_quotes']:
            is_single_quote = True

        inspections = {}

        # Issue messages for all double quotes if single quotes prevail (or overwise)
        if is_single_quote and file_discrete['double_quotes'] > 0.0:
            inspections[self.NEED_TO_USE_SINGLE_QUOTES] = {
                'message': self.inspections[self.NEED_TO_USE_SINGLE_QUOTES].format(discrete['single_quotes'] * 100),
                'lines': values['double_quotes']['lines'][:],
            }
        elif not is_single_quote and file_discrete['single_quotes'] > 0.0:
            inspections[self.NEED_TO_USE_DOUBLE_QUOTES] = {
                'message': self.inspections[self.NEED_TO_USE_DOUBLE_QUOTES].format(discrete['double_quotes'] * 100),
                'lines': values['single_quotes']['lines'][:],
            }

        return inspections
