import math
import re


class MaxFunctionLength:
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
        'function_too_long': ' In this repo functions are mostly written shorter. '
                             ' Maybe you need to split this function into parts.'
    }

    """ Number of lines in functions. Verbose version doesn't require specific logic. """

    def count(self, file, verbose=False):
        with open(file) as f:
            result = None
            name = None
            string_count = 0
            max_len = 0
            cur_len = 0
            for line in f:
                result = re.match(r'(def)|((    |\t)def)', line)
                if result is not None:
                    # print(cur_line)
                    # cur_func_line = cur_line
                    if cur_len > max_len:
                        max_len = cur_len + 1
                    cur_len = 0
                else:
                    cur_len += 1
            if cur_len > max_len:
                max_len = cur_len + 1
        return {max_len: 1}

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
