# pushgateway
## Introduction

The Prometheus Pushgateway is a simple HTTP server that allows data to be pushed to it, rather than pulled. It exists to allow ephemeral and batch jobs to expose their metrics to Prometheus. Since these kinds of jobs may not exist long enough to be scraped, they can instead push their metrics to a Pushgateway. The Pushgateway then exposes these metrics to Prometheus.

The Pushgateway acts as an intermediary, holding the pushed data until it is scraped by Prometheus. It supports pushing metrics from multiple sources, **each identified by a unique `job` label, and optionally additional labels**.

pushgateway github:https://github.com/prometheus/pushgateway

## Installation

To install the Pushgateway, you can download the binary package or use a package manager, but using Docker is more recommended. You can install the Pushgateway on any machine, and typically, only one Pushgateway server is needed to handle metrics from all sources. Here’s how you can set up the Pushgateway using Docker:

```shell
docker pull prom/pushgateway

docker run -d -p 9091:9091 prom/pushgateway
```

## Pushing Metrics to the Pushgateway

To push metrics to the Pushgateway, you can use the `curl` command-line tool or a custom application that sends HTTP requests. Additionally, there are third-party libraries available for various programming languages that simplify the process of sending metrics to the Pushgateway.

### Using `curl`

Here's an example of pushing a single metric to the Pushgateway:

```shell
curl -X POST http://{pushgateway_server}:{port}/metrics/job/myjob/instance/myinstance \
     --data 'my_metric{label="value"} 1.0'
```

This command pushes a metric named `my_metric` with the value `1.0` and a label `label` set to `value`.

### Using Third-Party Libraries

Several third-party libraries are available to help you integrate Pushgateway functionality into your applications. These libraries provide a higher-level API for sending metrics, making it easier to manage the interaction with the Pushgateway.

For example, in Python, you can use the `prometheus_client` library, the code is in `pusher.py`.