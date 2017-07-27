import math


class NestingLoops:
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

    """ Number of nesting loops in files. Verbose version doesn't require specific logic. """

    def count(self, file, verbose=False):
        # level = 0
        # begin = []
        # end = []
        # num_spaces = []
        # num_str = -1
        with open(file) as f:
            nests = 0
            max_nests = 0
            line_ind = 0
            prev_spaces = [0, 0]
            balance_list = [[0, 0]]
            i = 1
            was_cycle = False
            while True:
                s = f.readline()
                if not s:
                    break
                if self.is_spaces(s):
                    i += 1
                    continue

                spaces = self.count_spaces_pair(s)
                #print(i, spaces, prev_spaces, was_cycle)
                if spaces > prev_spaces and was_cycle:
                    nests += 1
                    balance_list.append(spaces)
                if spaces < prev_spaces:
                    while len(balance_list) > 0 and balance_list[-1] > spaces:
                        balance_list.remove(balance_list[-1])
                        nests -= 1

                cur_nests = 0
                dict = ["while ", "for ", "while(", "for("]
                for j in range(len(s)):
                    for word in dict:
                        if s[j: min(j + len(word), len(s))] == word:
                            cur_nests += 1
                was_cycle = cur_nests > 0

                if was_cycle and nests + cur_nests > max_nests:
                    max_nests = nests + cur_nests
                    line_ind = i

                prev_spaces = spaces
                i += 1

        result = {'max_nests': max_nests}
        if verbose:
            result['max_nests'] = {
                'count': max_nests,
                'lines': [line_ind],
            }
        return result

    def is_spaces(self, s):
        for x in s:
            if x != ' ' and x != '\t' and x != '\n':
                return False
        return True

    def count_spaces_pair(self, s):
        res = [0, 0]
        for x in s:
            if x == ' ':
                res[0] += 1
            if x == '\t':
                res[1] += 1
        return res

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
