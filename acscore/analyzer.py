from . import metrics


class Analyzer:
    configuration = metrics.IMPLEMENTED_METRICS

    def __init__(self, metrics, configuration=None):
        self.metrics = metrics
        if configuration:
            self.configuration = configuration
        self.process_metrics()

    def process_metrics(self):
        pass
