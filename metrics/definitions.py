from prometheus_client import Gauge, Counter, CollectorRegistry, generate_latest
from prometheus_client import multiprocess, start_http_server
import os

# Use a shared directory for multiprocess mode
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

# Define metrics with 'process' label automatically
response_time_metric = Gauge('uptimetrackr_response_time_ms', 'Response time in ms', ['url'], registry=registry)
status_code_metric = Gauge('uptimetrackr_http_status_code', 'HTTP status code', ['url'], registry=registry)
availability_metric = Gauge('uptimetrackr_available', '1 if site is up (200), 0 if not', ['url'], registry=registry)
error_counter = Counter('uptimetrackr_errors_total', 'Total number of failed checks', ['url'], registry=registry)
request_counter = Counter('uptimetrackr_total_requests', 'Total health checks sent', ['url'], registry=registry)

def update_metrics(url, status_code, response_time):
    request_counter.labels(url=url).inc()
    if isinstance(status_code, int):
        response_time_metric.labels(url=url).set(response_time)
        status_code_metric.labels(url=url).set(status_code)
        availability_metric.labels(url=url).set(1 if status_code == 200 else 0)
        if status_code != 200:
            error_counter.labels(url=url).inc()
    else:
        availability_metric.labels(url=url).set(0)
        error_counter.labels(url=url).inc()
