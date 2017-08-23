import math


def is_spaces(st):
    for x in st:
        if x == '#':
            return True
        if x != ' ' and x != '\t' and x != '\n':
            return False
    return True


class BlankBeforeMethod:
    """ Number of blank lines before method definition inside class
    in files. Verbose version doesn't require specific logic. """

    TOO_FEW_LINES = 'too_few_lines'
    TOO_MANY_LINES = 'too_many_lines'


    inspections = {
        TOO_FEW_LINES: 'Too few lines between methods, comparing to the repository.'
                       'Add new lines here.',
        TOO_MANY_LINES: 'Too many lines between methods, comparing to the repository!'
                        'Reduce lines here.',
    }

    discrete_groups = [
        {
            'name': '0',
            'from': 0,
            'to': 0,
        },
        {
            'name': '1',
            'from': 1,
            'to': 1,
        },
        {
            'name': '2',
            'from': 2,
            'to': 2,
        },
        {
            'name': '3+',
            'from': 3,
            'to': math.inf,
        },
    ]


    def count(self, file, verbose=False):
        # Count blank lines after method
        with open(file) as f:
            res = [0, 0, 0, 0]
            res_list = [[], [], [], []]

            blank = 0
            i = 0
            beginning = True
            for line in f.readlines():
                i += 1

                start = 0
                for x in line:
                    if x != ' ' and x != '\t' and x != '\n':
                        break
                    else:
                        start += 1
                if line[start: start + 4] == "def " and start > 0 and not beginning:
                    res[min(3, blank)] += 1
                    res_list[min(3, blank)].append(i)
                if is_spaces(line):
                    blank += 1
                else:
                    blank = 0

                beginning = False
                if line[start: start + 6] == "class ":
                    beginning = True

        # Form result
        result = {}

        if res[0] > 0:
            result['0'] = res[0]
        if res[1] > 0:
            result['1'] = res[1]
        if res[2] > 0:
            result['2'] = res[2]
        if res[3] > 0:
            result['3+'] = res[3]

        if verbose:
            if res[0] > 0:
                result['0'] = {
                    'count': res[0],
                    'lines': res_list[0],
                }
            if res[1] > 0:
                result['1'] = {
                    'count': res[1],
                    'lines': res_list[1],
                }
            if res[2] > 0:
                result['2'] = {
                    'count': res[2],
                    'lines': res_list[2],
                }
            if res[3] > 0:
                result['3+'] = {
                    'count': res[3],
                    'lines': res_list[3],
                }

        return result


    def discretize(self, values):
        discrete_values = {}
        sum = 0.0

        # Set initial values for groups to 0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0

        # Sum values for each group
        for value, count in values.items():
            for group in self.discrete_groups:
                if group['from'] <= int(value[0]) <= group['to']:
                    discrete_values[group['name']] += count
                    sum += count
                    continue

        # Normalize
        for key, value in discrete_values.items():
            discrete_values[key] = value / sum

        return discrete_values

    def inspect(self, discrete, values):
        inspections = {}

        # Inspections for 0 new lines between methods (if repository contains less than 50% of such a things)
        if discrete['0'] > 0.5:
            for nc_count in values.keys():
                if nc_count == '3+':
                    int_nc = 5
                else:
                    int_nc = int(nc_count)
                if 1 <= int_nc <= math.inf:
                    if self.TOO_MANY_LINES in inspections:
                        inspections[self.TOO_MANY_LINES]['lines'] += values[nc_count]['lines']
                        continue
                    inspections[self.TOO_MANY_LINES] = {
                        'message': self.inspections[self.TOO_MANY_LINES],
                        'lines': values[nc_count]['lines'],
                    }
        if discrete['1'] > 0.5:
            for nc_count in values.keys():
                if nc_count == '3+':
                    int_nc = 5
                else:
                    int_nc = int(nc_count)
                if 0 <= int_nc <= 0:
                    if self.TOO_FEW_LINES in inspections:
                        inspections[self.TOO_FEW_LINES]['lines'] += values[nc_count]['lines']
                        continue
                    inspections[self.TOO_FEW_LINES] = {
                        'message': self.inspections[self.TOO_FEW_LINES],
                        'lines': values[nc_count]['lines'][:],
                    }
                if int_nc > 1:
                    if self.TOO_MANY_LINES in inspections:
                        inspections[self.TOO_MANY_LINES]['lines'] += values[nc_count]['lines']
                        continue
                    inspections[self.TOO_MANY_LINES] = {
                        'message': self.inspections[self.TOO_MANY_LINES],
                        'lines': values[nc_count]['lines'][:],
                    }
        if discrete['2'] > 0.5:
            for nc_count in values.keys():
                if nc_count == '3+':
                    int_nc = 5
                else:
                    int_nc = int(nc_count)
                if 0 <= int_nc <= 1:
                    if self.TOO_FEW_LINES in inspections:
                        inspections[self.TOO_FEW_LINES]['lines'] += values[nc_count]['lines']
                        continue
                    inspections[self.TOO_FEW_LINES] = {
                        'message': self.inspections[self.TOO_FEW_LINES],
                        'lines': values[nc_count]['lines'][:],
                    }
                if int_nc > 3:
                    if self.TOO_MANY_LINES in inspections:
                        inspections[self.TOO_MANY_LINES]['lines'] += values[nc_count]['lines']
                        continue
                    inspections[self.TOO_MANY_LINES] = {
                        'message': self.inspections[self.TOO_MANY_LINES],
                        'lines': values[nc_count]['lines'][:],
                    }
        if discrete['3+'] > 0.5:
            for nc_count in values.keys():
                if nc_count == '3+':
                    int_nc = 5
                else:
                    int_nc = int(nc_count)
                if 0 <= int_nc <= 2:
                    if self.TOO_FEW_LINES in inspections:
                        inspections[self.TOO_FEW_LINES]['lines'] += values[nc_count]['lines']
                        continue
                    inspections[self.TOO_FEW_LINES] = {
                        'message': self.inspections[self.TOO_FEW_LINES],
                        'lines': values[nc_count]['lines'][:],
                    }
        # Sort line numbers
        for key in inspections.keys():
            inspections[key]['lines'] = sorted(inspections[key]['lines'])
        return inspections
