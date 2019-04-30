"""
Base classes to be inherited from for Search and EarlyTerminate algorithms
"""


class Search():
    def _metric_from_run(self, sweep_config, run):
        metric_name = sweep_config['metric']['name']

        maximize = False
        if 'goal' in sweep_config['metric']:
            if sweep_config['metric']['goal'] == 'maximize':
                maximize = True

        if metric_name in run.summaryMetrics:
            metric = run.summaryMetrics[metric_name]
        else:
            # maybe should do something other than erroring
            raise ValueError(
                "Couldn't find summary metric {}".format(metric_name))

        if maximize:
            metric = -metric

        return metric

    def next_run(self, sweep):
        """Called each time an agent requests new work.
        Args:
            sweep: <defined above>
        Returns:
            None if all work complete for this sweep. A dictionary of configuration
            parameters for the next run.
        """
        raise NotImplementedError


class EarlyTerminate():
    def _load_metric_name_and_goal(self, sweep_config):
        if not 'metric' in sweep_config:
            raise ValueError("Key 'metric' required for early termination")

        self.metric_name = sweep_config['metric']['name']

        self.maximize = False
        if 'goal' in sweep_config['metric']:
            if sweep_config['metric']['goal'] == 'maximize':
                self.maximize = True

    def _load_run_metric_history(self, run):
        metric_history = []
        for line in run.history:
            if self.metric_name in line:
                m = line[self.metric_name]
                metric_history.append(m)

        if self.maximize:
            metric_history = [-m for m in metric_history]

        return metric_history

    def stop_runs(self, sweep_config, runs):
        return [], {}