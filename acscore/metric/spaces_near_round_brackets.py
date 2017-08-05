import re

class SpacesNearRoundBrackets:
    """ Checks whether round brackets are divided from content with spaces. """
    NEED_SPACES = 'spaces'
    NEED_NO_SPACES = 'no_spaces'

    discrete_groups = [
        { 'name': 'spaces' },
        { 'name': 'no_spaces' },
    ]

    inspections = {
        NEED_SPACES: 'Mostly spaces are put near round brackets, '
                                   'maybe you need to add spaces near round brackets here.',
        NEED_NO_SPACES: 'No spaces near round brackets are used in the source code, '
                                   'maybe it\'s better to remove spaces here.',
    }

    def count(self, file, verbose=False):
        # Count all square brackets with spaces before or after its usage
        with open(file) as f:

            brackets_with_spaces_count = 0
            brackets_with_no_spaces_count = 0
            spaces_usage_lines = []
            no_spaces_usage_lines = []
            reg_open_space =  re.compile(r'\(\s')
            reg_close_space = re.compile(r'\s\)')
            reg_open_no_space = re.compile(r'\(\S')
            reg_close_no_space = re.compile(r'\S\)')

            line_number = 0
            for line in f.readlines():
                line_number += 1

                amount_open_brackets_spaces = len(reg_open_space.findall(line))
                amount_open_brackets_no_spaces = len(reg_open_no_space.findall(line))
                amount_close_brackets_spaces = len(reg_close_space.findall(line))
                amount_close_brackets_no_spaces = len(reg_close_no_space.findall(line))

                brackets_with_spaces_count += amount_open_brackets_spaces
                brackets_with_spaces_count += amount_close_brackets_spaces
                brackets_with_no_spaces_count += amount_open_brackets_no_spaces
                brackets_with_no_spaces_count += amount_close_brackets_no_spaces

                if amount_open_brackets_spaces or amount_close_brackets_spaces:
                    spaces_usage_lines.append(line_number)
                if amount_open_brackets_no_spaces or amount_close_brackets_no_spaces:
                    no_spaces_usage_lines.append(line_number)

        # Form result
        result = {
            'spaces': brackets_with_spaces_count,
            'no_spaces': brackets_with_no_spaces_count,
        }

        if verbose:
            result['spaces'] = {
                'count': brackets_with_spaces_count,
                'lines': spaces_usage_lines,
            }
            result['no_spaces'] = {
                'count': brackets_with_no_spaces_count,
                'lines': spaces_usage_lines,
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

        # Check if spaces existance is prevailing
        spaces = False
        if discrete['spaces'] > discrete['no_spaces']:
            spaces = True

        inspections = {}

        # Issue messages for all round brackets where spaces after or before prevail (or overwise)
        if spaces and file_discrete['no_spaces'] > 0.0:
            inspections[self.NEED_SPACES] = {
                'message': self.inspections[self.NEED_SPACES].format(discrete['spaces'] * 100),
                'lines': values['no_spaces']['lines'][:],
            }
        elif not spaces and file_discrete['spaces'] > 0.0:
            inspections[self.NEED_NO_SPACES] = {
                'message': self.inspections[self.NEED_NO_SPACES].format(discrete['no_spaces'] * 100),
                'lines': values['spaces']['lines'][:],
            }

        return inspections
