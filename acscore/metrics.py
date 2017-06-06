import re
import ast


INF=99999


def count_spaces(string):
    count = 0
    for i in string:
        if (i != ' '):
            continue
        else:
            count += 1
    return count


def count_strings(file):
    lines = sum(1 for line in file)
    return lines


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


def classes_count(file):
    with open(file) as f:
        classes_amount = 0
        result = True
        for i in f:
            result = re.match(r'[ ]*class ', i)
            if (result is not None):
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
            if (result1 is not None):
                begin.append(num_str)
            result2 = re.search(r'^[ ]*while', x)
            if (result2 is not None):
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
                if (num_spaces[j] <= num_spaces[i]):
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
        while ((begin[i] != 99999) and (end[j] != 99999)):
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


def analyze_names(file):
    with open(file) as f:
        root = ast.parse(f.read())
        names = sorted({node.id for node in ast.walk(root) if isinstance(node, ast.Name)})
        underscore = 0
        camelcase = 0
        for i in names:
            if i in ["False", "True", "None"]:
                continue
            if i.isupper():
                continue
            for j in i:
                if j is "_":
                    underscore += 1
                   # print "under"
                    break
                if j.isupper():
                    #print "camel"
                    camelcase += 1
    print(underscore, camelcase)
    return { "underscore": underscore,
             "camelcase": camelcase }


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
