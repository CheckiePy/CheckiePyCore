import sys
import os

from . import counter


def main():
    if len(sys.argv) != 2:
        print('Specify file or directory as single command line argument for metrics count')
        return
    path = sys.argv[1]
    if not os.path.isfile(path) and not os.path.isdir(path):
        print('Specified string is not file or directory')
        return
    cntr = counter.Counter()
    cfg = ['file_length']
    if os.path.isfile(path):
        metrics = cntr.metrics_for_file(path, cfg)
    else:
        metrics = cntr.metrics_for_dir(path, cfg)
    print(metrics)

if __name__ == '__main__':
    main()