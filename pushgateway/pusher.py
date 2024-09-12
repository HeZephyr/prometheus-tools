import csv
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

class PrometheusPusher:
    def __init__(self, metric_name: str, description: str, job_name: str, pushgateway_url: str = 'localhost:9091'):
        """
        Initialize an instance of PrometheusPusher.
        
        :param metric_name: The name of the metric.
        :param description: A description of the metric.
        :param job_name: Job name used to identify the source.
        :param pushgateway_url: URL of the Pushgateway service, default is localhost:9091.
        """
        self.metric_name = metric_name
        self.description = description
        self.job_name = job_name
        self.pushgateway_url = pushgateway_url
        self.registry = CollectorRegistry()
        self.gauge = None

    def create_gauge(self, label_names: list):
        """
        Create a gauge metric with labels.
        
        :param label_names: List of label names.
        """
        self.gauge = Gauge(self.metric_name, self.description, label_names, registry=self.registry)
    
    def push_metrics(self, label_values: list):
        """
        Push the metric value to the Pushgateway.
        
        :param label_values: List of label values.
        """
        if not self.gauge:
            print('Error: Gauge is not created')
            return
        self.gauge.labels(*label_values).set(1)
        try:
            push_to_gateway(self.pushgateway_url, job=self.job_name, registry=self.registry)
            print(f'Successfully pushed metrics for {label_values}')
        except Exception as e:
            print(f'Failed to push metrics for {label_values}. Error: {e}')
    
    def push_metrics_from_csv(self, csv_file_path: str):
        """
        Read data from a CSV file and push metrics.
        
        :param csv_file_path: Path to the CSV file.
        """
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            # Get the label names (first row)
            label_names = next(reader)
            self.create_gauge(label_names)
            for row in reader:
                if len(row) != len(label_names):
                    print(f"Warning: Ignoring row with incorrect number of columns: {row}")
                    continue
                self.push_metrics(row)

# Example CSV file format:
# label1, label2
# value1, value2
# ...

# Main entry point
if __name__ == '__main__':
    # Set CSV file path and other parameters
    csv_file_path = 'example_data.csv'
    metric_name = 'example_metric'
    description = 'An example metric for demonstration purposes.'
    job_name = "example_job"
    pushgateway_url = 'slcx-grafana.calix.local:9091'

    # Create an instance of PrometheusPusher and push data from CSV file
    pusher = PrometheusPusher(metric_name, description, job_name, pushgateway_url)
    pusher.push_metrics_from_csv(csv_file_path)