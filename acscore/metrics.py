import re
import ast

IMPLEMENTED_METRICS = [
    'FileLength',
    'FunctionNameCase',
    'NestingLoops',
    'MaxFunctionLength',
    #'FunctionLength',
    'ClassNameCase',
    'IndentType',
]

INF = 99999


class FileLength:
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
            'to': INF,
        },
    ]
    inspections = {
        'too_many_lines': ' File too long ' 
                          ' According to the repo scan we recommend you to split this file into parts. '
    }

    """ Number of lines in file. Verbose version doesn't require specific logic. """

    def count(self, file, verbose=False):
        i = 0
        with open(file) as f:
            for i, _ in enumerate(f, 1):
                pass
        return {'{0}'.format(i): 1}

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
        for group in self.discrete_groups:
            if group['from'] <= int(value) <= group['to']:
                value_group = group
                percent += discrete[group['name']]
            elif int(value) <= group['from']:
                # If file contains fewer lines it's ok
                percent += discrete[group['name']]
        inspections = {}
        too_many_lines = 'too_many_lines'
        if percent < 0.05:
            inspections[too_many_lines] = {'message': self.inspections[too_many_lines].format(5)}
        elif percent < 0.1:
            inspections[too_many_lines] = {'message': self.inspections[too_many_lines].format(10)}
        elif percent < 0.2:
            inspections[too_many_lines] = {'message': self.inspections[too_many_lines].format(20)}
        return inspections


class FunctionNameCase:
    NEED_TO_USE_CAMEL_CASE = 'need_to_use_camelcase'
    NEED_TO_USE_UNDERSCORE = 'need_to_use_underscore'
    NO_STYLE = 'no_style'
    discrete_groups = [
        {
            'name': 'underscore',
        },
        {
            'name': 'camelcase',
        },
        {
            'name': 'other',
        },
    ]
    inspections = {
        NEED_TO_USE_CAMEL_CASE: ' According to the repo scan we recommend you to use camelcase '
                                ' Instead of underscore in this function name',
        NEED_TO_USE_UNDERSCORE: ' According to the repo scan we recommend you to use underscore '
                                ' Instead of camelcase in this function name',
        NO_STYLE: 'Underscore and camel case mixed in same name.',
    }

    """ Number of underscored and camel cased names of functions in file. """

    def count(self, file, verbose=False):
        with open(file) as f:
            root = ast.parse(f.read())
            names = [(node.name, node.lineno) for node in ast.walk(root) if isinstance(node, ast.FunctionDef)]
            underscore_count = 0
            underscore_lines = []
            camelcase_count = 0
            camelcase_lines = []
            other_count = 0
            other_lines = []
            for name, line in names:
                # Underscored or in camel case with underscore (i.e. "other")
                if '_' in name:
                    if name.startswith('__'):
                        continue
                    if any(ch.isupper() for ch in name) or ('__' in name):
                        other_count += 1
                        other_lines.append(line)
                    else:
                        underscore_count += 1
                        underscore_lines.append(line)
                # In camel case
                elif any(ch.isupper() for ch in name):
                    camelcase_count += 1
                    camelcase_lines.append(line)
                else:
                    # One word without underscores and capital letters (don't count this)
                    pass
        result = {
            'underscore': underscore_count,
            'camelcase': camelcase_count,
            'other': other_count,
        }
        if verbose:
            result['underscore'] = {
                'count': underscore_count,
                'lines': underscore_lines,
            }
            result['camelcase'] = {
                'count': camelcase_count,
                'lines': camelcase_lines,
            }
            result['other'] = {
                'count': other_count,
                'lines': other_lines,
            }
        return result

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0
        for group, count in values.items():
            discrete_values[group] = count
            sum += count
        for group, count in discrete_values.items():
            if sum != 0:
                discrete_values[group] = count / sum
        return discrete_values

    def inspect(self, discrete, values):
        for_discretization = {}
        for key, value in values.items():
            for_discretization[key] = value['count']
        file_discrete = self.discretize(for_discretization)
        is_camelcase = False
        if file_discrete['camelcase'] > file_discrete['underscore']:
            is_camelcase = True
        inspections = {}
        if file_discrete['other'] > 0.0:
            inspections[self.NO_STYLE] = {
                'message': self.inspections[self.NO_STYLE],
                'lines': values['other']['lines'],
            }
        if is_camelcase and file_discrete['underscore'] > 0.0:
            inspections[self.NEED_TO_USE_CAMEL_CASE] = {
                'message': self.inspections[self.NEED_TO_USE_CAMEL_CASE].format(discrete['camelcase'] * 100),
                'lines': values['underscore']['lines'],
            }
        elif not is_camelcase and file_discrete['camelcase'] > 0.0:
            inspections[self.NEED_TO_USE_UNDERSCORE] = {
                'message': self.inspections[self.NEED_TO_USE_UNDERSCORE].format(discrete['underscore'] * 100),
                'lines': values['camelcase']['lines'],
            }
        return inspections


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
            'to': INF,
        },
    ]
    inspections = {
        'too_many_loops': ' You definitely can write this file using less loops! ',
        'more_loops_than_needed': ' Too many loops comparing to the repository. ',
    }

    """ Number of nesting loops in files. Verbose version doesn't require specific logic. """

    def count(self, file, verbose=False):
        level = 0
        begin = []
        end = []
        num_spaces = []
        num_str = -1
        with open(file) as f:
            while True:
                x = f.readline()
                if not x: break
                num_str += 1
                result1 = re.search(r'^([ ]|[\t])*for', x)
                if result1 is not None:
                    begin.append(num_str)
                result2 = re.search(r'^([ ]|[\t])*while', x)
                if result2 is not None:
                    begin.append(num_str)
                    # print num_str
            f.seek(0)
            num_str = -1
            prev = 0
            while True:
                x = f.readline()
                if not x: break
                if x == "\n":
                    num_spaces.append(0)
                    continue
                prev = count_spaces(x)
                num_spaces.append(prev)
            f.seek(0)
            num_str = count_strings(f)
            f.seek(0)
            for i in begin:
                for j in range(i + 1, num_str):
                    if num_spaces[j] <= num_spaces[i]:
                        end.append(j)
                        break
            end.sort()
            if not end:
                for i in begin:
                    end.append(num_str)
            nests = 0
            max_nests = 0
            end.append(99999)
            begin.append(99999)
            i = 0
            j = 0
            first_entry = 0
            while (begin[i] != 99999) and (end[j] != 99999):
                # print begin[i]
                # print end[j]
                if begin[i] < end[j]:
                    nests += 1
                    if max_nests < nests:
                        max_nests = nests
                        first_entry = begin[i] + 1
                    i += 1
                if begin[i] >= end[j]:
                    nests -= 1
                    j += 1
        result = {'max_nests': max_nests}
        if verbose:
            result['max_nests'] = {
                'count': max_nests,
                'lines': [first_entry],
            }
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
            'to': INF,
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


class ClassNameCase:
    NEED_TO_USE_CAMEL_CASE = 'need_to_use_camelcase'
    NEED_TO_USE_UNDERSCORE = 'need_to_use_underscore'
    NO_STYLE = 'no_style'
    discrete_groups = [
        {
            'name': 'underscore',
        },
        {
            'name': 'camelcase',
        },
        {
            'name': 'other',
        },
    ]
    inspections = {
        NEED_TO_USE_CAMEL_CASE: ' According to the repo scan we recommend you to use camelcase '
                                ' Instead of underscore in this class definition ',
        NEED_TO_USE_UNDERSCORE: ' According to the repo scan we recommend you to use underscore '
                                ' Instead of camelcase in this class definition ',
        NO_STYLE: 'Underscore and camel case mixed in same class name.',
    }

    """ Number of underscored and camel cased names of classes in file. """

    def count(self, file, verbose=False):
        with open(file) as f:
            root = ast.parse(f.read())
            names = [(node.name, node.lineno) for node in ast.walk(root) if isinstance(node, ast.ClassDef)]
            underscore_count = 0
            underscore_lines = []
            camelcase_count = 0
            camelcase_lines = []
            other_count = 0
            other_lines = []
            for name, line in names:
                # Underscored or in camel case with underscore (i.e. "other")
                if '_' in name:
                    if any(ch.isupper() for ch in name):
                        other_count += 1
                        other_lines.append(line)
                    else:
                        underscore_count += 1
                        underscore_lines.append(line)
                # In camel case
                elif any(ch.isupper() for ch in name):
                    camelcase_count += 1
                    camelcase_lines.append(line)
                else:
                    # One word without underscores and capital letters (don't count this)
                    pass
        result = {
            'underscore': underscore_count,
            'camelcase': camelcase_count,
            'other': other_count,
        }
        if verbose:
            result['underscore'] = {
                'count': underscore_count,
                'lines': underscore_lines,
            }
            result['camelcase'] = {
                'count': camelcase_count,
                'lines': camelcase_lines,
            }
            result['other'] = {
                'count': other_count,
                'lines': other_lines,
            }
        return result

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0
        for group, count in values.items():
            discrete_values[group] = count
            sum += count
        for group, count in discrete_values.items():
            if sum != 0:
                discrete_values[group] = count / sum
        return discrete_values

    def inspect(self, discrete, values):
        for_discretization = {}
        for key, value in values.items():
            for_discretization[key] = value['count']
        file_discrete = self.discretize(for_discretization)
        is_camelcase = False
        if file_discrete['camelcase'] > file_discrete['underscore']:
            is_camelcase = True
        inspections = {}
        if file_discrete['other'] > 0.0:
            inspections[self.NO_STYLE] = {
                'message': self.inspections[self.NO_STYLE],
                'lines': values['other']['lines'],
            }
        if is_camelcase and file_discrete['underscore'] > 0.0:
            inspections[self.NEED_TO_USE_CAMEL_CASE] = {
                'message': self.inspections[self.NEED_TO_USE_CAMEL_CASE].format(discrete['camelcase'] * 100),
                'lines': values['underscore']['lines'],
            }
        elif not is_camelcase and file_discrete['camelcase'] > 0.0:
            inspections[self.NEED_TO_USE_UNDERSCORE] = {
                'message': self.inspections[self.NEED_TO_USE_UNDERSCORE].format(discrete['underscore'] * 100),
                'lines': values['camelcase']['lines'],
            }
        return inspections


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
            'to': INF,
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



class IndentType:
    NEED_TO_USE_TABS = 'need_to_use_tabs'
    NEED_TO_USE_SPACES = 'need_to_use_spaces'
    discrete_groups = [
        {
            'name': 'tabs',
        },
        {
            'name': 'spaces',
        },
    ]
    inspections = {
        NEED_TO_USE_TABS: ' Tabs are used in {0}% of your code, but these are spaces. ',
        NEED_TO_USE_SPACES: ' Spaces are used in {0}% of your code, but these are tabs. ',
    }

    """ Number of tabs and spaces indents in file. """

    def count(self, file, verbose=False):
        with open(file) as f:
            spaces_count = 0
            tabs_count = 0
            for line in f:
                if line[:2] == '  ':
                   spaces_count += 1
                if line[:1] == '\t':
                    tabs_count += 1
        if tabs_count > spaces_count:
            result = {
                'spaces': 0,
                'tabs': 1,
            }
        else:
            result = {
                'spaces': 1,
                'tabs': 0,
            }
        return result

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0
        for group, count in values.items():
            discrete_values[group] = count
            sum += count
        for group, count in discrete_values.items():
            discrete_values[group] = count / sum
        return discrete_values

    def inspect(self, discrete, values):
        for_discretization = {}
        for key, value in values.items():
            for_discretization[key] = value
        file_discrete = self.discretize(for_discretization)
        is_tab = False
        if discrete['tabs'] > discrete['spaces']:
            is_tab = True
        inspections = {}
        if is_tab and file_discrete['spaces'] > 0.0:
            inspections[self.NEED_TO_USE_TABS] = {
                'message': self.inspections[self.NEED_TO_USE_TABS].format(discrete['tabs'] * 100)
            }
        elif not is_tab and file_discrete['tabs'] > 0.0:
            inspections[self.NEED_TO_USE_SPACES] = {
                'message': self.inspections[self.NEED_TO_USE_SPACES].format(discrete['spaces'] * 100)
            }
        return inspections

# Todo: incorrect
def name_case(file, verbose=False):
    """ Number of underscored and camel cased names in file. """
    with open(file) as f:
        root = ast.parse(f.read())
        print('***', list(ast.walk(root)), '***')
        names = sorted({(node.id, node.lineno) for node in ast.walk(root) if isinstance(node, ast.Name)})
        # names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
        underscore = 0
        underscore_lines = []
        camelcase = 0
        camelcase_lines = []
        # for name in names:
        for name, line in names:
            if name in ['False', 'True', 'None']:
                continue
            if name.isupper():
                continue
            for character in name:
                if character is '_':
                    underscore += 1
                    underscore_lines.append((name, line))
                    # underscore_lines.append(name)
                    break
                if character.isupper():
                    camelcase += 1
                    camelcase_lines.append((name, line))
                    # camelcase_lines.append(name)
    result = {
        'underscore': underscore,
        'camelcase': camelcase
    }
    if verbose:
        result['underscore'] = {
            'count': underscore,
            'lines': underscore_lines,
        }
        result['camelcase'] = {
            'count': camelcase,
            'lines': camelcase_lines,
        }
    return result


def count_spaces(string):
    count = 0
    for i in string:
        if (i != '\t') and (i != ' '):
            break
        else:
            if (i == '\t'):
                count += 4
            if (i == ' '):
                count += 1
    return count

def count_strings(file):
    lines = sum(1 for line in file)
    return lines


def function_count(file):
    with open(file) as f:
        func_amount = 0
        result = True
        for i in file:
            result = re.match(r'[ ]*def ', i)
            if result is not None:
                func_amount += 1
    return {func_amount: 1}


def classes_count(file):
    with open(file) as f:
        classes_amount = 0
        result = True
        for i in f:
            result = re.match(r'[ ]*class ', i)
            if result is not None:
                classes_amount += 1
    print(classes_amount)
    return {classes_amount: 1}

