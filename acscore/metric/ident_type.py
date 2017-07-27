import ast
import re


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
