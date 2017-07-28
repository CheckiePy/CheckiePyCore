class IndentType:
    """ It checks tabs or spaces used in source code file. """

    NEED_TO_USE_TABS = 'need_to_use_tabs'
    NEED_TO_USE_SPACES = 'need_to_use_spaces'

    discrete_groups = [
        { 'name': 'tabs' },
        { 'name': 'spaces' },
    ]

    inspections = {
        NEED_TO_USE_TABS: 'Tabs are used in most part of your code, but here are spaces.',
        NEED_TO_USE_SPACES: 'Spaces are used in most part of your code, but here are tabs.',
    }

    def count(self, file, verbose=False):
        # Check if code lines starting from tabs or spaces
        with open(file) as f:
            spaces_count = 0
            tabs_count = 0
            for line in f:
                if line[:2] == '  ':
                    spaces_count += 1
                if line[:1] == '\t':
                    tabs_count += 1

        # Form result
        result = {
            'spaces': 0,
            'tabs': 0,
        }
        if tabs_count > spaces_count:
            result['tabs'] = 1
        elif tabs_count < spaces_count:
            result['spaces'] = 1

        return result

    # TODO: move to base class
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
            discrete_values[group] = count / sum

        return discrete_values

    def inspect(self, discrete, values):
        for_discretization = {}

        # Extract count from verbose output (see docs)
        for key, value in values.items():
            for_discretization[key] = value

        file_discrete = self.discretize(for_discretization)

        # Check if tabs or spaces are prevailing
        is_tab = False
        if discrete['tabs'] > discrete['spaces']:
            is_tab = True

        # Suggest to use tabs (if it is prevailing for entire project) in file with spaces or overwise
        inspections = {}
        if is_tab and file_discrete['spaces'] > 0.0:
            inspections[self.NEED_TO_USE_TABS] = {
                'message': self.inspections[self.NEED_TO_USE_TABS]
            }
        elif not is_tab and file_discrete['tabs'] > 0.0:
            inspections[self.NEED_TO_USE_SPACES] = {
                'message': self.inspections[self.NEED_TO_USE_SPACES]
            }

        return inspections
