import math


class NestingLoops:
    """ Number of nesting loops in files. Verbose version doesn't require specific logic. """

    LOOP_KEYWORDS = ["while ", "for ", "while(", "for("]
    TOO_MANY_LOOPS = 'too_many_loops'
    EXTREMELY_MANY_LOOPS = 'extremely_many_loops'

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
        TOO_MANY_LOOPS: 'Too deep loop nesting comparing to the repository.',
        EXTREMELY_MANY_LOOPS: 'Extremely deep loop nesting.',
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

        # Set initial values for groups to 0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0

        # Sum values for each group
        for value, count in values.items():
            for group in self.discrete_groups:
                if group['from'] <= int(value) <= group['to']:
                    discrete_values[group['name']] += count
                    sum += count
                    continue

        # Normalize
        for key, value in discrete_values.items():
            discrete_values[key] = value / sum

        return discrete_values

    def inspect(self, discrete, values):
        inspections = {}

        # Inspections for nested loops with depth from 3 to 4 (if repository contains less than 10% of such loops)
        if discrete['From3To4'] >= 0.1:
            for loop_count in values.keys():
                if 3 <= int(loop_count) <= 4:
                    if self.TOO_MANY_LOOPS in inspections:
                        inspections[self.TOO_MANY_LOOPS]['lines'] += values[loop_count]['lines']
                        continue
                    inspections[self.TOO_MANY_LOOPS] = {
                        'message': self.inspections[self.TOO_MANY_LOOPS],
                        'lines': values[loop_count]['lines'][:],
                    }

        # Inspections for nested loops with deep more than 4
        for loop_count in values.keys():
            if int(loop_count) >= 5:
                if self.EXTREMELY_MANY_LOOPS in inspections:
                    inspections[self.EXTREMELY_MANY_LOOPS]['lines'] += values[loop_count]['lines']
                    continue
                inspections[self.EXTREMELY_MANY_LOOPS] = {
                    'message': self.inspections[self.EXTREMELY_MANY_LOOPS],
                    'lines': values[loop_count]['lines'][:],
                }

        # Sort line numbers
        for key in inspections.keys():
            inspections[key]['lines'] = sorted(inspections[key]['lines'])

        return inspections
