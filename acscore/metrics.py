import re

def file_length(file):
    i = 0
    with open(file) as f:
        for i, _ in enumerate(f, 1):
            pass
    return {i: 1}


def function_count(file):
    with open(file) as f:
        func_amount = 0
        result = True
        for i in file:
            result = re.match(r'[ ]*def ', i)
            if (result is not None):
                func_amount += 1
    return {func_amount: 1}


def function_length(file = "/home/flerchy/acscore/acscore/metrics.py"):
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
            if (inside == True):
                string_count += 1
            if ((result is not None) and (inside == True)):
                lengths_of_func[name] = string_count
                string_count = 0
                inside = False
            if ((result is not None) and (inside == False)):
                name = re.search('(?<=def )\w+\(.*\)', i)
                #(name)
                string_count = 0
                inside = True
            result2 = re.match(r'[a-z]|[A-Z]', i)
            if ((result2 is not None) and (result is None) and (inside == True)):
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