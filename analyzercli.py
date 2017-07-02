import sys
import os
import json

from acscore import analyzer, counter


def main():
    if len(sys.argv) != 3:
        print('Specify file for analyze and file with metrics')
        return
    file_path = sys.argv[1]
    metrics_path = sys.argv[2]
    if not os.path.isfile(file_path) or not os.path.isfile(metrics_path):
        print('Specified string is not file')
        return
    with open(metrics_path, 'r') as metrics_file:
        metrics = json.loads(metrics_file.read())
    cntr = counter.Counter()
    file_metrics = cntr.metrics_for_file(file_path, verbose=True)
    anlzr = analyzer.Analyzer(metrics)
    inspections = anlzr.inspect(file_metrics)
    result = {
        'file_metrics': file_metrics,
        'inspections': inspections,
    }
    print(json.dumps(result, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()