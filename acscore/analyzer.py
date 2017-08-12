from . import metrics


class Analyzer:
    configuration = metrics.IMPLEMENTED_METRICS

    def __init__(self, metrics, configuration=None):
        self.metrics = metrics
        if configuration:
            self.configuration = configuration
        self.process_metrics()

    def process_metrics(self):
        self.metric_instances = {}
        self.discrete_values = {}
        for metric, value in self.metrics.items():
            metric_class = getattr(metrics, metric)
            self.metric_instances[metric] = metric_class()
            self.discrete_values[metric] = self.metric_instances[metric].discretize(value)

    def inspect(self, file_metrics):
        inspections = {}
        for metric, values in file_metrics.items():
            if metric in self.metric_instances:
                inspections[metric] = self.metric_instances[metric].inspect(self.discrete_values[metric], values)
        return inspections
