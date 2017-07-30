

## Getting started

[![Build Status](https://travis-ci.org/acsproj/acscore.svg?branch=master)](https://travis-ci.org/acsproj/acscore)

### 1. Prerequisites

* Python 3.5

### 2. Setup

```
git clone https://github.com/acsproj/acscore.git
cd acscore
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 3. How to use

#### 3.1. From command line

Get metrics for file or directory:

```
python3 countercli.py <path to file or directory>
```

Get inspections for file or directory:
```
python3 analyzecli.py <path to file for analyze> <path to file with metrics>
```

#### 3.2. From code

* Look at analyzercli.py and countercli.py for guidance.

#### 3.3. Run tests

```
python3 test.py
```

### 4. Implemented metrics

- [x] FileLength
- [x] FunctionNameCase
- [x] ClassNameCase
- [x] IndentType
- [x] NestingLoops

### 5. Report format

```
{
    "metric_name1":
    {
        "metric_value1": count_of_occurences,
        "metric_value2": ...,
        ...
    },
    "metric_name2":
    {
        ...
    },
    ...
}
```

### 6. Metric implementation notes

#### 6.1. Structure

Metrics should be implemented as class with three methods:

```python
class MetricName:
    """ Metric meaning. """
    def count(self, file, verbose=False):
        """
        Method to count this metric in file.
        Verbose flag specified if lines are needed. 
        """
        pass

    def discretize(self, values):
        """
        Some metric may have very wide range (continuous).
        For instance, it can be file length in lines.
        Metric values like this should be discretized
        up to 10 different values.
        """
        pass

    def inspect(self, discrete, values):
        """
        This method compares counted metrics for file
        (values param) with discrete values for this
        metric (discrete param) and returns inspection
        messages with line number of code style violation.
        Values to this method should be passed in verbose
        format.
        """
        pass
```

#### 6.2. Placing

* Metric class should be placed in separate file under metric directory.

* Class name of implemented metric should be registered in IMPLEMENTED_METRICS dictionary in metrics.py.

#### 6.3. Output

##### 6.3.1. Count method

* Count method should return an output in next format (non verbose):

```
{
    "metric_value1": count_of_occurences,
    "metric_value2": ...,
    ...
}
```

and in verbose format:
```
{
    "metric_value1":
    {
        "count": number,
        "lines": [list_with_line_numbers],
    },
    "metric_value2": ...,
    ...
}
```

##### 6.3.2. Discretize method

```
{
    "metric_value1": percent_in_float_format,
    "metric_value2": ...,
    ...
}
```

For example 10% in float format is 0.1.

##### 6.3.3. Inspect method

```
{
    "inspection_name1":
    {
        "message": "Inspection message.",
        "lines": [numbers_of_lines],
    },
    "inspection_name2": ...,
    ...
}
```

If inspection isn't applicable to some line then "lines" property should be omitted.

# License

The MIT License (MIT) Copyright (c) 2017 Artem Ustimov, Marina Belyanova

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.