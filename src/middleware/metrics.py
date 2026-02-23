"""Prometheus metrics"""
from prometheus_client import Counter, Histogram, Gauge

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Named active_connections to match main.py import
active_connections = Gauge(
    'http_connections_active',
    'Active HTTP connections'
)

error_count = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['endpoint']
)

agent_execution_time = Histogram(
    'agent_execution_seconds',
    'Agent execution time',
    ['node']
)
