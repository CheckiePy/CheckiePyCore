import re
import ast

IMPLEMENTED_METRICS = [
    'FileLength',
    'FunctionNameCase',
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
        'too_many_lines': 'Less than {0}% of files have approximately same size.'
                          ' Maybe you need to split this file in parts.'
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
        NEED_TO_USE_CAMEL_CASE: 'Camel case is used in {0}% of code, but here underscore is used.',
        NEED_TO_USE_UNDERSCORE: 'Underscore is used in {0}% of code, but here camel case is used.',
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


# Todo: incorrect
def name_case(file, verbose=False):
    """ Number of underscored and camel cased names in file. """
    with open(file) as f:
        root = ast.parse(f.read())
        print('***', list(ast.walk(root)), '***')
        names = sorted({(node.id, node.lineno) for node in ast.walk(root) if isinstance(node, ast.Name)})
        #names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
        underscore = 0
        underscore_lines = []
        camelcase = 0
        camelcase_lines = []
        #for name in names:
        for name, line in names:
            if name in ['False', 'True', 'None']:
                continue
            if name.isupper():
                continue
            for character in name:
                if character is '_':
                    underscore += 1
                    underscore_lines.append((name, line))
                    #underscore_lines.append(name)
                    break
                if character.isupper():
                    camelcase += 1
                    camelcase_lines.append((name, line))
                    #camelcase_lines.append(name)
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
        if i != ' ':
            continue
        else:
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


def function_length(file):
    with open(file) as f:
        lengths_of_func = {}
        result = None
        inside = False
        name = None
        string_count = 0
        for i in f:
            #print(i)
            result = re.match(r'[ ]*def', i)
            #print(result)
            if inside == True:
                string_count += 1
            if (result is not None) and (inside is True):
                lengths_of_func[name] = string_count
                string_count = 0
                inside = False
            if (result is not None) and (inside is False):
                name = re.search('(?<=def )\w+\(.*\)', i)
                #(name)
                string_count = 0
                inside = True
            result2 = re.match(r'[a-z]|[A-Z]', i)
            if (result2 is not None) and (result is None) and (inside is True):
                lengths_of_func[name] = string_count
                string_count = 0
                inside = False
            if name not in lengths_of_func.keys():
                lengths_of_func[name] = string_count
    res = {}
    for i in lengths_of_func.keys():
        res[lengths_of_func[i]] = 0
    for i in lengths_of_func.keys():
        res[lengths_of_func[i]] += 1
    return res


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


def count_loop_nesting(file):
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
            result1 = re.search(r'^[ ]*for', x)
            if result1 is not None:
                begin.append(num_str)
            result2 = re.search(r'^[ ]*while', x)
            if result2 is not None:
                begin.append(num_str)
            #print num_str
        #print begin
        f.seek(0)
        num_str = -1
        prev = 0
        while True:
            x = f.readline()
            if not x: break
            if x == "\n": num_spaces.append(prev)
            prev = count_spaces(x)
            num_spaces.append(prev)
        #print num_spaces
        f.seek(0)
        num_str = count_strings(f)
        f.seek(0)
        for i in begin:
            #print i
            for j in range(i+1, num_str):
                if num_spaces[j] <= num_spaces[i]:
                    #print j
                    end.append(j)
                    break
        end.sort()
        if not end:
            for i in begin:
                end.append(num_str)
        #print end
        nests = 0
        max_nests = 0
        end.append(INF)
        begin.append(INF)
        i = 0
        j = 0
        while (begin[i] != 99999) and (end[j] != 99999):
                #print begin[i]
                #print end[j]
                if begin[i] < end[j]:
                    nests += 1
                    if max_nests < nests:
                        max_nests = nests
                    i += 1
                if begin[i] >= end[j]: 
                    nests -= 1
                    j += 1
    print(max_nests)
    return { max_nests: 1 }


# Todo: redefenition (look at first function)
def count_spaces(file):
    with open(file) as f:
        count = 0
        for line in file:
            if (line[:4]) != "    ":
                continue
            else:
                count += 1
    return { "spaces": count }


def count_tabs(file):
    with open(file) as f:
        count = 0
        for line in file:
            for i in line:
                if (i is not "\t"):
                    break    
                else:
                    count += 1
    return { "tabs": count }
