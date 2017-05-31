

## Getting started

### Prerequisites

* Python 3.5

### Setup

```
git clone https://github.com/acsproj/acscore.git
cd acscore
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### How to use

```
python3 main.py <path to file or directory>
```

### Implemented metrics

* File length (in lines)

### Report format

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

### Metric implementation notes

* Metrics should be implemented as functions with the only parameter (path to file)

* Metric functions should be placed in metrics.py file

* Metric function should return an output in next format:

```
{
    "metric_value1": count_of_occurences,
    "metric_value2": ...,
    ...
}
```

## License

The MIT License (MIT) Copyright (c) 2017 Artem Ustimov

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.