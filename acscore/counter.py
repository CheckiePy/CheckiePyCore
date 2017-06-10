import os

from . import metrics


class Counter:
    configuration = metrics.IMPLEMENTED_METRICS

    def metrics_for_file(self, file, configuration=None, verbose=False):
        if not configuration:
            configuration = self.configuration
        calculated = {}
        for metric_name in configuration:
            metric_class = getattr(metrics, metric_name)
            metric_instance = metric_class()
            calculated[metric_name] = metric_instance.count(file, verbose)
        return calculated

    def merge_metrics(self, dst, src):
        for key, value in src.items():
            if key in dst:
                for value_key in value:
                    if value_key in dst[key]:
                        dst[key][value_key] += value[value_key]
                    else:
                        dst[key][value_key] = value[value_key]
            else:
                 dst[key] = value

    def metrics_for_dir(self, dir, configuration=None):
        if not configuration:
            configuration = self.configuration
        calculated = {}
        for root, subdirs, files in os.walk(dir):
            for subdir in subdirs:
                calc_for_dir = self.metrics_for_dir(os.path.join(root, subdir), configuration)
                self.merge_metrics(calculated, calc_for_dir)
            for file in files:
                if file.endswith('.py'):
                    calc_for_file = self.metrics_for_file(os.path.join(root, file), configuration)
                    self.merge_metrics(calculated, calc_for_file)
        return calculated
