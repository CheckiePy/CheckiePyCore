class ImportOrder:
    """ Imports specific order. Verbose version doesn't require specific logic. """

    NEED_SORTING = 'need_sorting'

    discrete_groups = [
        {
            'name': 'sorted',
        },
        {
            'name': 'not_sorted',
        },
        {
            'name': 'no_imports',
        }
    ]

    inspections = {
        NEED_SORTING: ' Scanned repo uses sorting in it\'s files, '
                      ' we recommend you to sort imports here.'
    }

    def count(self, file, verbose=False):
        with open(file) as f:
            words = []
            imports = False
            cnt = 0
            for line in f.readlines():
                if line[:6] == 'import':
                    if not imports:
                        cnt += 1
                        if cnt > 1:
                            imports = True
                    words.append(line[7:])
            some = sorted(words)
            if some == words:
                return {"is_sorted": 1}
            elif imports:
                return {"not_sorted": 1}
            else:
                return {"no_imports": 1}

    def discretize(self, values):
        discrete_values = {}
        sum = 0.0

        # Set initial values for each group to 0
        for group in self.discrete_groups:
            discrete_values[group['name']] = 0

        # Sum group values for each file
        for value, count in values.items():
            for group in self.discrete_groups:
                discrete_values[value] += count
                sum += count
                continue

        # Normalize values
        for key, value in discrete_values.items():
            discrete_values[key] = value / sum
        return discrete_values

    def inspect(self, discrete, values):

        inspections = {}

        # Param values in this case should contain single value (for single file)
        value = list(values.keys())[0]
        if value == "no_imports":
            return inspections
        # Find percent of files with length equal (or more) to length of value discrete group
        percent = 0.0
        for group in self.discrete_groups:
            if group["name"] == value:
                percent += discrete[group["name"]]
        # If less 1 % of files have approximately same length (or more) then generate message
        if percent < 0.5:
            inspections[self.NEED_SORTING] = {'message': self.inspections[self.NEED_SORTING]}

        return inspections
