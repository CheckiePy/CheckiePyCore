import math
import re


class FunctionLength:
    discrete_groups = [
        {
            'name': 'From0To10',
            'from': 0,
            'to': 10,
        },
        {
            'name': 'From11To40',
            'from': 11,
            'to': 40,
        },
        {
            'name': 'From41To100',
            'from': 41,
            'to': 100,
        },
        {
            'name': 'From101To250',
            'from': 101,
            'to': 250,
        },
        {
            'name': 'From250To1000',
            'from': 250,
            'to': 1000,
        },
        {
            'name': 'From1000ToInf',
            'from': 1000,
            'to': math.inf,
        },
    ]
    inspections = {
        'function_too_long': 'Less than {0}% of your functions have approximately same size.'
                             ' Maybe you need to split function in this file in parts.'
    }

    """ Number of lines in functions. Verbose version doesn't require specific logic. """

    def count(self, file, verbose=False):
        with open(file) as f:
            lengths_of_func = {}
            result = None
            inside = False
            name = None
            string_count = 0
            cur_line = 0
            cur_func_line = 0
            for i in f:
                cur_line += 1
                # print(i)
                result = re.match(r'[ ]*def', i)
                # print(result)
                if inside == True:
                    string_count += 1
                if (result is not None) and (inside is True):
                    # print(cur_line)
                    # cur_func_line = cur_line
                    lengths_of_func[cur_func_line] = string_count - 2
                    string_count = 0
                    inside = False
                if (result is not None) and (inside is False):
                    # print(cur_line)
                    name = re.search('(?<=def )\w+\(.*\)', i)
                    # if name is not None:
                    #    print(cur_func_line, name)
                    cur_func_line = cur_line
                    # (name)
                    string_count = 0
                    inside = True
                result2 = re.match(r'[a-z]|[A-Z]', i)
                if (result2 is not None) and (result is None) and (inside is True):
                    lengths_of_func[cur_func_line] = string_count
                    string_count = 0
                    inside = False
        res = dict((v, k) for k, v in lengths_of_func.items())
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
        inspections = {}
        value = (list(values.keys()) or [None])[0]
        if not value:
            return inspections
        percent = 0.0
        for group in self.discrete_groups:
            if group['from'] <= int(value) <= group['to']:
                # value_group = group
                percent += discrete[group['name']]
            elif int(value) <= group['from']:
                # If function contains fewer lines it's ok
                percent += discrete[group['name']]
        func_too_long = 'function_too_long'
        if percent < 0.05:
            inspections[func_too_long] = {'message': self.inspections[func_too_long].format(5)}
        elif percent < 0.1:
            inspections[func_too_long] = {'message': self.inspections[func_too_long].format(10)}
        elif percent < 0.2:
            inspections[func_too_long] = {'message': self.inspections[func_too_long].format(20)}
        return inspections
