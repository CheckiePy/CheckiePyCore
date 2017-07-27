import ast


class FunctionNameCase:
    """ Number of underscored and camel cased names of functions in file. """

    NEED_TO_USE_CAMEL_CASE = 'need_to_use_camelcase'
    NEED_TO_USE_UNDERSCORE = 'need_to_use_underscore'
    NO_STYLE = 'no_style'

    discrete_groups = [
        { 'name': 'underscore' },
        { 'name': 'camelcase' },
        { 'name': 'other' },
    ]

    inspections = {
        NEED_TO_USE_CAMEL_CASE: 'According to the repo scan we recommend you to use camelcase '
                                'instead of underscore in this function name.',
        NEED_TO_USE_UNDERSCORE: 'According to the repo scan we recommend you to use underscore '
                                'instead of camelcase in this function name.',
        NO_STYLE: 'Underscore and camel case mixed in the same name.',
    }

    def count(self, file, verbose=False):
        with open(file) as f:
            # Find all function names in source code file
            root = ast.parse(f.read())
            names = [(node.name, node.lineno) for node in ast.walk(root) if isinstance(node, ast.FunctionDef)]

            # Group all function names in three groups
            underscore_count = 0
            underscore_lines = []
            camelcase_count = 0
            camelcase_lines = []
            other_count = 0
            other_lines = []
            for name, line in names:
                # Underscore or camel case with underscore (i.e. "other")
                if '_' in name:
                    # Skip special names like __str__
                    if name.startswith('__') and name.endswith('__'):
                        continue
                    # If underscored name contains big letters or multiple neighboring underscores
                    if any(ch.isupper() for ch in name) or ('__' in name):
                        other_count += 1
                        other_lines.append(line)
                    else:
                        underscore_count += 1
                        underscore_lines.append(line)
                # Camel case
                elif any(ch.isupper() for ch in name):
                    camelcase_count += 1
                    camelcase_lines.append(line)
                else:
                    # Single word without underscores and capital letters (don't count this)
                    pass

        # Form result
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

        # Extract count for discretization ( { 'key': { 'count': 1, 'lines': [1] } } => { 'key' : 1 }
        for key, value in values.items():
            for_discretization[key] = value['count']

        file_discrete = self.discretize(for_discretization)

        # Find out which style is prevail in file
        is_camelcase = False
        if file_discrete['camelcase'] > file_discrete['underscore']:
            is_camelcase = True

        inspections = {}

        # Issue messages for all bad styles names
        if file_discrete['other'] > 0.0:
            inspections[self.NO_STYLE] = {
                'message': self.inspections[self.NO_STYLE],
                'lines': values['other']['lines'],
            }

        # Issue messages for all undersored names if camel case is prevail (or overwise)
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
