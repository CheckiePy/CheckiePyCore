import re


class SpacesNearBraces:
    """ Checks whether braces are divided from content with spaces. """

    NEED_SPACES = 'spaces'
    NEED_NO_SPACES = 'no_spaces'
    NEED_NEW_LINES = 'new_lines'

    discrete_groups = [
        { 'name': 'spaces' },
        { 'name': 'no_spaces' },
        { 'name': 'new_lines'}
    ]

    inspections = {
        NEED_SPACES: 'Mostly spaces are put near braces, '
                     'maybe you need to add spaces near braces here.',
        NEED_NO_SPACES: 'No spaces near braces are used in the source code, '
                        'maybe it\'s better to remove spaces here.',
        NEED_NEW_LINES: 'New lines are used in source code mostly, '
                        'you should use them here too',
    }

    def count(self, file, verbose=False):
        # Count all square brackets with spaces before or after its usage
        with open(file) as f:

            brackets_with_spaces_count = 0
            brackets_with_no_spaces_count = 0
            brackets_with_new_line_count = 0

            spaces_usage_lines = []
            no_spaces_usage_lines = []
            new_line_usage_lines = []

            reg_open_space = re.compile(r'(\{ )')
            reg_close_space = re.compile(r'( \})')
            reg_open_new_line = re.compile(r'(\{\n)')
            reg_close_new_line = re.compile(r'\n\}')
            reg_open_no_space = re.compile(r'\{\S')
            reg_close_no_space = re.compile(r'\S\}')

            line_number = 0
            single_quote = False
            double_quote = False
            for line in f.readlines():
                line_number += 1

                no_quote = ""
                for i in range(len(line)):
                    if not single_quote and not double_quote:
                        no_quote += line[i]
                    if i > 0 and line[i - 1] == '\\':
                        continue
                    if line[i] == '\'':
                        single_quote = not single_quote
                    if line[i] == '\"':
                        double_quote = not double_quote

                amount_open_brackets_spaces = len(reg_open_space.findall(no_quote))
                amount_open_brackets_no_spaces = len(reg_open_no_space.findall(no_quote))
                amount_close_brackets_spaces = len(reg_close_space.findall(no_quote))
                amount_close_brackets_no_spaces = len(reg_close_no_space.findall(no_quote))
                amount_open_brackets_new_line = len(reg_open_new_line.findall(no_quote))
                amount_close_brackets_new_line = len(reg_close_new_line.findall(no_quote))

                brackets_with_spaces_count += amount_open_brackets_spaces
                brackets_with_spaces_count += amount_close_brackets_spaces
                brackets_with_no_spaces_count += amount_open_brackets_no_spaces
                brackets_with_no_spaces_count += amount_close_brackets_no_spaces
                brackets_with_new_line_count += amount_open_brackets_new_line
                brackets_with_new_line_count += amount_close_brackets_new_line

                if amount_open_brackets_spaces or amount_close_brackets_spaces:
                    spaces_usage_lines.append(line_number)
                if amount_open_brackets_no_spaces or amount_close_brackets_no_spaces:
                    no_spaces_usage_lines.append(line_number)
                if amount_open_brackets_new_line or amount_close_brackets_new_line:
                    new_line_usage_lines.append(line_number)

        # Form result
        result = {
            'spaces': brackets_with_spaces_count,
            'no_spaces': brackets_with_no_spaces_count,
            'new_lines': brackets_with_new_line_count,
        }

        if verbose:
            result['spaces'] = {
                'count': brackets_with_spaces_count,
                'lines': spaces_usage_lines,
            }
            result['no_spaces'] = {
                'count': brackets_with_no_spaces_count,
                'lines': no_spaces_usage_lines,
            }
            result['new_lines'] = {
                'count': brackets_with_new_line_count,
                'lines': new_line_usage_lines,
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
        no_spaces = False

        if max(discrete['spaces'], discrete['no_spaces'], discrete['new_lines']) == discrete['spaces']:
            spaces = True
        elif max(discrete['spaces'], discrete['no_spaces'], discrete['new_lines']) == discrete['no_spaces']:
            no_spaces = True

        inspections = {}

        # Issue messages for all braces where spaces after or before prevail (or overwise)
        if spaces:
            if file_discrete['no_spaces'] > 0.0:
                if self.NEED_SPACES not in inspections:
                    inspections[self.NEED_SPACES] = {
                        'message': self.inspections[self.NEED_SPACES],
                        'lines': []
                    }
                inspections[self.NEED_SPACES]['lines'] += values['no_spaces']['lines']
            if file_discrete['new_lines'] > 0.0:
                if self.NEED_SPACES not in inspections:
                    inspections[self.NEED_SPACES] = {
                        'message': self.inspections[self.NEED_SPACES],
                        'lines': []
                    }
                inspections[self.NEED_SPACES]['lines'] += values['new_lines']['lines']
        elif no_spaces:
            if file_discrete['spaces'] > 0.0:
                if self.NEED_NO_SPACES not in inspections:
                    inspections[self.NEED_NO_SPACES] = {
                        'message': self.inspections[self.NEED_NO_SPACES],
                        'lines': []
                    }
                inspections[self.NEED_NO_SPACES]['lines'] += values['spaces']['lines']
            if file_discrete['new_lines'] > 0.0:
                if self.NEED_NO_SPACES not in inspections:
                    inspections[self.NEED_NO_SPACES] = {
                        'message': self.inspections[self.NEED_NO_SPACES],
                        'lines': []
                    }
                inspections[self.NEED_NO_SPACES]['lines'] += values['new_lines']['lines']
        else:
            if file_discrete['spaces'] > 0.0:
                if self.NEED_NEW_LINES not in inspections:
                    inspections[self.NEED_NEW_LINES] = {
                        'message': self.inspections[self.NEED_NEW_LINES],
                        'lines': []
                    }
                inspections[self.NEED_NEW_LINES]['lines'] += values['spaces']['lines']
            if file_discrete['no_spaces'] > 0.0:
                if self.NEED_NEW_LINES not in inspections:
                    inspections[self.NEED_NEW_LINES] = {
                        'message': self.inspections[self.NEED_NEW_LINES],
                        'lines': []
                    }
                inspections[self.NEED_NEW_LINES]['lines'] += values['no_spaces']['lines']

        return inspections
