import math


class NestingLoops:
    """ Number of nesting loops in files. Verbose version doesn't require specific logic. """

    LOOP_KEYWORDS = ["while ", "for ", "while(", "for("]

    discrete_groups = [
        {
            'name': 'From0To2',
            'from': 0,
            'to': 2,
        },
        {
            'name': 'From3To4',
            'from': 3,
            'to': 4,
        },
        {
            'name': 'From5ToInf',
            'from': 5,
            'to': math.inf,
        },
    ]
    inspections = {
        'too_many_loops': ' You definitely can write this file using less loops! ',
        'more_loops_than_needed': ' Too many loops comparing to the repository. ',
    }

    def count(self, file, verbose=False):
        with open(file) as f:
            previous_indentation = 0
            is_loop = False
            nesting = 0
            to_next_line = False
            line_number = 0
            latest_keyword_line = 0
            loops = []
            for line in f.readlines():
                line_number += 1
                trimmed_line = line.strip()
                for keyword in self.LOOP_KEYWORDS:
                    # If line with loop definition
                    if trimmed_line.startswith(keyword):
                        latest_keyword_line = line_number
                        indentation = line.index(keyword)
                        if not is_loop:
                            is_loop = True
                            nesting = 1
                        else:
                            if previous_indentation < indentation:
                                nesting += 1
                            else:
                                loops.append((nesting, latest_keyword_line))
                                nesting = 1
                        previous_indentation = indentation
                        to_next_line = True
                        break

                # Go to next line if current line contains loop header
                if to_next_line:
                    to_next_line = False
                    continue

                # If line inside loop body
                if is_loop:
                    if previous_indentation >= len(line) - len(trimmed_line):
                        loops.append((nesting, latest_keyword_line))
                        previous_indentation = 0
                        is_loop = False
                        nesting = 0

            # If file ends with loop then record this loop info
            if is_loop:
                loops.append((nesting, latest_keyword_line))

            # Form result
            result = {}
            for loop in loops:
                nesting = str(loop[0])
                if verbose:
                    if nesting in result:
                        result[nesting]['count'] += 1
                        result[nesting]['lines'].append(loop[1])
                    else:
                        result[nesting] = {'count': 1, 'lines': [loop[1]]}
                else:
                    if nesting in result:
                        result[nesting] += 1
                    else:
                        result[nesting] = 1

            return result

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
        print(values['max_nests']['count'])
        for group in self.discrete_groups:
            if group['from'] <= values['max_nests']['count'] <= group['to']:
                value_group = group
                percent += discrete[group['name']]
            elif int(values['max_nests']['count']) <= group['from']:
                # If file contains fewer loops it's ok
                percent += discrete[group['name']]
        inspections = {}
        too_many_loops = 'too_many_loops'
        more_loops_than_needed = 'more_loops_than_needed'
        if value_group['name'] == 'From5ToInf':
            inspections[too_many_loops] = {
                'message': self.inspections[too_many_loops],
                'lines': values['max_nests']['line'],
            }
            inspections[too_many_loops] = {
                'message': self.inspections[too_many_loops],
                'lines': values['max_nests']['line'],
            }
        elif percent < 0.1:
            inspections[more_loops_than_needed] = {
                'message': self.inspections[more_loops_than_needed],
                'lines': values['max_nests']['line'],
            }
        elif percent < 0.2:
            inspections[more_loops_than_needed] = {
                'message': self.inspections[more_loops_than_needed],
                'lines': values['max_nests']['line'],
            }
        return inspections
