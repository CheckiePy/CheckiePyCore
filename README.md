

## Getting started

[![Build Status](https://travis-ci.org/acsproj/acscore.svg?branch=master)](https://travis-ci.org/acsproj/acscore)

### 1. Prerequisites

* Python 3.5

### 2. Setup

```
git clone https://github.com/CheckiePy/CheckiePyCore.git
cd CheckiePyCore
python3 -m venv venv
source venv/bin/activate
```

### 3. How to use

#### 3.1. From a command line

Get metrics for a file or a directory:

```
python3 countercli.py <path to file or directory>
```

Get inspections for a file or a directory:
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
- [x] NestingLoops
- [x] ClassNameCase
- [x] IndentType
- [x] QuotesType
- [x] SpacesNearRoundBrackets
- [x] SpacesNearBraces
- [x] SpacesNearSquareBrackets
- [x] ImportOrder
- [x] BlankBeforeFunction
- [x] BlankBeforeClass
- [x] BlankBeforeMethod

### 5. A report format

```
{
    "metric_name1":
    {
        "metric_value1": number_of_occurences,
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

#### 6.1. A structure

Metrics should be implemented as class with three methods:

```python
class MetricName:
    """ Metric's meaning. """
    def count(self, file, verbose=False):
        """
        The method to count the metric from the 'file'.
        The 'verbose' flag is specified when you need to get line numbers where the metric occurs. 
        """
        pass

    def discretize(self, values):
        """
        Some metrics can have a very wide range (continuous).
        For instance, it can be a file length in lines.
        Metric's values like that should be discretized
        up to 10 different values.
        """
        pass

    def inspect(self, discrete, values):
        """
        This method compares counted metrics for a file
        (values param) with discrete values for this
        metric (discrete param) and returns inspection
        messages with line numbers of code style violations.
        Values should be passed to this method in verbose
        format.
        """
        pass
```

#### 6.2. Placing

* Metric's class should be placed in a separate file under the metric directory.

* A class name of implemented metric should be registered in IMPLEMENTED_METRICS dictionary in metrics.py.

#### 6.3. Output

##### 6.3.1. The 'count' method

* The 'count' method should return an output in the next format (non verbose):

```
{
    "metric_value1": number_of_occurences,
    "metric_value2": ...,
    ...
}
```

and in the verbose format:
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

##### 6.3.2. The 'discretize' method

```
{
    "metric_value1": percent_in_a_float_format,
    "metric_value2": ...,
    ...
}
```

For example, 10% is 0.1 in the float format.

##### 6.3.3. The 'inspect' method

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

If inspection isn't applicable to some line then 'lines' property should be omitted.

# License

[MIT](/LICENSE)
